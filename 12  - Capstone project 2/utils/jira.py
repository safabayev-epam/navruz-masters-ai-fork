# utils/jira.py

import requests
import base64
import streamlit as st
from constants import JIRA_URL, JIRA_USERNAME, JIRA_PROJECT_KEY

def create_jira_ticket(summary: str, description: str) -> (bool, str):
    if "JIRA_API_TOKEN" not in st.secrets:
        st.error("JIRA_API_TOKEN not found in Streamlit secrets.")
        return False, "JIRA API Token not configured."

    jira_api_token = st.secrets["JIRA_API_TOKEN"]
    url = f"{JIRA_URL}/rest/api/2/issue/"
    auth = base64.b64encode(f"{JIRA_USERNAME}:{jira_api_token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"},
        }
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        if resp.status_code == 201:
            issue_key = resp.json().get("key", "")
            return True, issue_key
        else:
            return False, resp.text
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}"
