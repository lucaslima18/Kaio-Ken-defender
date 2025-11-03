from dataclasses import dataclass


@dataclass
class ScannerTemplateSchema:
    template: str
    template_id: str
    template_url: str
    template_path: str


@dataclass
class ScannerIssueSchema:
    issue_name: str
    issue_author: str
    issue_tags: list[str]
    issue_description: str
    issue_reference: list[str]
    issue_severity: str


@dataclass
class ScannerCompleteSchema(ScannerTemplateSchema, ScannerIssueSchema):
    host: str
    port: str
    description: str
    type: str
    matcher_name: str
    matched_at: str
    matcher_status: bool
    timestamp: str
