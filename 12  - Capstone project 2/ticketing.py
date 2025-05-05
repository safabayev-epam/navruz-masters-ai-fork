# ticketing.py

import os
from jira import JIRA

from config import JIRA_EMAIL, JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_PROJECT_KEY

def get_jira_client() -> JIRA:
    return JIRA(
        server=JIRA_SERVER_URL,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )

def create_jira_ticket(name: str, email: str, title: str, description: str) -> str:
    """
    Create a Jira issue and return its key (e.g. "PROJ-123").
    """
    jira = get_jira_client()
    issue_fields = {
        "project": {"key": JIRA_PROJECT_KEY},
        "summary": title,
        "description": f"*Reporter:* {name} <{email}>\n\n{description}",
        "issuetype": {"name": "Task"}
    }
    issue = jira.create_issue(fields=issue_fields)
    return issue.key
