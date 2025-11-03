import json
import time

import pika

from app.shared.config import config


class RabbitMQPublisher:
    """RabbitMQ publisher for sending scan jobs"""

    def __init__(self):
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self, max_retries=5, retry_delay=5):
        """Establish connection to RabbitMQ with retry logic"""
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

                print(
                    f"✓ Connected to RabbitMQ at {config.RABBITMQ_HOST}:{config.RABBITMQ_PORT}"
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

    def publish_scan_job(self, scan_id, target):
        """Publish a scan job to the queue"""
        try:
            message = {"scan_id": scan_id, "target": target}

            self.channel.basic_publish(
                exchange="",
                routing_key=config.RABBITMQ_QUEUE,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                ),
            )

            print(f"📤 Published scan job: {scan_id} for target: {target}")
            return True

        except Exception as e:
            print(f"✗ Failed to publish scan job: {e}")
            # Try to reconnect
            try:
                self._connect()
                return self.publish_scan_job(scan_id, target)
            except:
                return False

    def close(self):
        """Close the connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()


# Singleton instance
_publisher = None


def get_publisher():
    """Get or create publisher instance"""
    global _publisher
    if _publisher is None:
        _publisher = RabbitMQPublisher()
    return _publisher
