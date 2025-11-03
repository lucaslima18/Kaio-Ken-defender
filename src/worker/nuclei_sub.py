import json
import signal
import sys
import time
from datetime import datetime

import pika

from app.api.models import Finding, Scan, ScanStatus
from app.shared.config import config
from app.shared.database import get_db, init_db
from app.worker.scanner import NucleiScanner


class ScanWorker:
    """RabbitMQ consumer that processes scan jobs"""

    def __init__(self):
        self.connection = None
        self.channel = None
        self.scanner = NucleiScanner()
        self.should_stop = False

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n⚠️  Received signal {signum}. Shutting down gracefully...")
        self.should_stop = True
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        sys.exit(0)

    def connect(self, max_retries=10, retry_delay=5):
        """Connect to RabbitMQ with retry logic"""
        for attempt in range(max_retries):
            try:
                credentials = pika.PlainCredentials(
                    config.RABBITMQ_USER, config.RABBITMQ_PASSWORD
                )
                parameters = pika.ConnectionParameters(
                    host=config.RABBITMQ_HOST,
                    port=config.RABBITMQ_PORT,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300,
                )

                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()

                # Declare queue as durable
                self.channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)

                # Set QoS to process one message at a time
                self.channel.basic_qos(prefetch_count=1)

                print(
                    f"✓ Worker connected to RabbitMQ at {config.RABBITMQ_HOST}:{config.RABBITMQ_PORT}"
                )
                return

            except Exception as e:
                print(
                    f"✗ Failed to connect to RabbitMQ (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise Exception(
                        f"Could not connect to RabbitMQ after {max_retries} attempts"
                    )

    def process_scan(self, scan_id, target):
        """Process a single scan job"""
        print(f"\n{'='*70}")
        print(f"🔍 Processing scan {scan_id}")
        print(f"🎯 Target: {target}")
        print(f"{'='*70}\n")

        try:
            # Update scan status to running
            with get_db() as session:
                scan = session.query(Scan).filter(Scan.id == scan_id).first()
                if not scan:
                    print(f"✗ Scan {scan_id} not found in database")
                    return

                scan.status = ScanStatus.RUNNING
                session.commit()

            print(f"⏳ Scan status: RUNNING")

            # Execute Nuclei scan
            findings = self.scanner.scan(target)

            # Store findings in database
            with get_db() as session:
                scan = session.query(Scan).filter(Scan.id == scan_id).first()

                if not scan:
                    print(f"✗ Scan {scan_id} not found")
                    return

                # Add findings
                for finding_data in findings:
                    finding = Finding(
                        scan_id=scan_id,
                        template_id=finding_data["template_id"],
                        name=finding_data["name"],
                        severity=finding_data["severity"],
                        matched_at=finding_data["matched_at"],
                        host=finding_data["host"],
                        type=finding_data["type"],
                        metadata=finding_data["metadata"],
                    )
                    session.add(finding)

                # Update scan
                scan.status = ScanStatus.COMPLETED
                scan.completed_at = datetime.utcnow()
                scan.findings_count = len(findings)

                session.commit()

            print(f"\n{'='*70}")
            print(f"✅ Scan {scan_id} completed successfully")
            print(f"📊 Found {len(findings)} vulnerabilities")
            print(f"{'='*70}\n")

        except Exception as e:
            print(f"\n{'='*70}")
            print(f"❌ Error processing scan {scan_id}: {e}")
            print(f"{'='*70}\n")

            # Update scan status to failed
            try:
                with get_db() as session:
                    scan = session.query(Scan).filter(Scan.id == scan_id).first()
                    if scan:
                        scan.status = ScanStatus.FAILED
                        scan.completed_at = datetime.utcnow()
                        scan.error_message = str(e)
                        session.commit()
            except Exception as db_error:
                print(f"✗ Failed to update scan status: {db_error}")

    def callback(self, ch, method, properties, body):
        """Callback function for processing messages"""
        try:
            # Parse message
            message = json.loads(body)
            scan_id = message.get("scan_id")
            target = message.get("target")

            if not scan_id or not target:
                print(f"✗ Invalid message format: {message}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            # Process the scan (BLOQUEIA AQUI até terminar)
            self.process_scan(scan_id, target)

            # Acknowledge message DEPOIS de processar
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"✗ Error in callback: {e}")
            # Reject and requeue message on error
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start(self):
        """Start consuming messages"""
        print(f"\n{'='*70}")
        print(f"⚙️  Worker starting...")
        print(f"📥 Queue: {config.RABBITMQ_QUEUE}")
        print(f"⏸️  Press CTRL+C to exit")
        print(f"{'='*70}\n")

        self.channel.basic_consume(
            queue=config.RABBITMQ_QUEUE, on_message_callback=self.callback
        )

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping worker...")
            self.channel.stop_consuming()
        finally:
            if self.connection and not self.connection.is_closed:
                self.connection.close()


def main():
    """Main entry point for worker"""
    print("\n🚀 Initializing Scan Worker...")

    # Initialize database
    init_db()

    # Create and start worker
    worker = ScanWorker()
    worker.connect()
    worker.start()


if __name__ == "__main__":
    main()
