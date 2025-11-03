from dataclasses import dataclass
import json
import subprocess
from shared.schemas.scanner_schema import ScannerCompleteSchema
from shared.utils.log_handler import LogHandler

logger = LogHandler(logger_name=__name__)


class NucleiScanner:
    def __init__(
        self, timeout: int = 120, severities: str = "critical,high,medium,low"
    ) -> None:
        self.timeout = timeout
        self.severities = severities

    def exec(self, target: str) -> ScannerSchema:
        command = self._set_command(target=target)
        logger.info("executing Nuclei scan on {target}")
        logger.info(f"Command: {' '.join(command)}")
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return self._cleanup_findings(
            findings=self._extract_vulnerabilities(
                process=process
            )
        )

    def _set_command(self, target: str) -> list[str]:
        return [
            "nuclei",
            "-u",
            target,
            "-jsonl",
            "-severity",
            self.severities,
            "-silent",
            "-no-color",
        ]

    def _extract_vulnerabilities(self, process: subprocess.Popen) -> list[dict]:
        stdout, stderr = process.communicate()

        if stderr:
            logger.warn(f"Nuclei stderr: {stderr}")

        findings = []
        for line in stdout.strip().split("\n"):
            if line.strip():
                try:
                    value = json.loads(line)
                    findings.append(value)
                    logger.info(f"Encontrado: {value['info']['name']} - {value['info']['severity']}")
                except json.JSONDecodeError as e:
                    logger.error(f"Erro ao parsear linha: {line[:100]}... | Erro: {e}")
                    continue

        logger.info(f"Scan completo. Total: {len(findings)} vulnerabilidades")
        return findings

    def _cleanup_findings(self, findings: list[dict]) -> list[ScannerCompleteSchema]:
        scanner_findings_formatted = []
        for finding in findings:
            scanner_findings_formatted.append(ScannerCompleteSchema(
                issue_name=finding["info"]["name"],
                issue_author=finding["info"]["author"][0],
                issue_tags=finding["info"]["tags"],
                issue_description=finding["info"]["description"]
                
            ))
            



# class NucleiScannerExcluir:
#     """Wrapper for Nuclei security scanner"""

#     def __init__(
#         self, timeout: int = 0, severities: str = "critical,high,medium,low,info"
#     ):
#         self.timeout = timeout
#         self.severities = severities

#     def scan(self, target):
#         """
#         Execute Nuclei scan on target

#         Args:
#             target (str): URL to scan

#         Returns:
#             list: List of finding dictionaries
#         """
#         findings = []

#         try:
#             # Build Nuclei command
#             command = [
#                 "nuclei",
#                 "-u",
#                 target,
#                 "-jsonl",
#                 "-severity",
#                 self.severities,
#                 "-silent",
#                 "-no-color",
#             ]

#             print(f"Executing Nuclei scan on {target}")
#             print(f"Command: {' '.join(command)}")

#             # Execute Nuclei
#             process = subprocess.Popen(
#                 command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
#             )

#             # Parse JSONL output line by line
#             try:
#                 stdout, stderr = process.communicate(timeout=self.timeout)

#                 if stderr:
#                     print(f"Nuclei stderr: {stderr}")

#                 # Process each JSON line
#                 for line in stdout.strip().split("\n"):
#                     if not line.strip():
#                         continue

#                     try:
#                         result = json.loads(line)

#                         # Extract vulnerability data
#                         finding = {
#                             "template_id": result.get("template-id", ""),
#                             "name": result.get("info", {}).get("name", ""),
#                             "severity": result.get("info", {}).get(
#                                 "severity", "unknown"
#                             ),
#                             "matched_at": result.get("matched-at", ""),
#                             "host": result.get("host", ""),
#                             "type": result.get("type", ""),
#                             "metadata": json.dumps(
#                                 {
#                                     "matcher_name": result.get("matcher-name", ""),
#                                     "tags": result.get("info", {}).get("tags", []),
#                                     "reference": result.get("info", {}).get(
#                                         "reference", []
#                                     ),
#                                     "curl_command": result.get("curl-command", ""),
#                                     "extracted_results": result.get(
#                                         "extracted-results", []
#                                     ),
#                                 }
#                             ),
#                         }

#                         findings.append(finding)
#                         print(f"Found: {finding['name']} [{finding['severity']}]")

#                     except json.JSONDecodeError as e:
#                         print(f"Failed to parse JSON: {line[:100]}... Error: {e}")
#                         continue

#                 print(f"Scan completed. Found {len(findings)} vulnerabilities")

#             except subprocess.TimeoutExpired:
#                 process.kill()
#                 raise Exception(f"Scan timeout after {self.timeout} seconds")

#             return findings

#         except FileNotFoundError:
#             raise Exception("Nuclei binary not found")
#         except Exception as e:
#             print(f"Error during scan: {e}")
#             raise e
