# config.py

import os
from dotenv import load_dotenv
load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Jira
JIRA_EMAIL       = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN   = os.getenv("JIRA_API_TOKEN")
JIRA_SERVER_URL  = os.getenv("JIRA_SERVER_URL")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# Company info
COMPANY_NAME   = "SN"
SUPPORT_EMAIL  = "safabayevnavruz@gmail.com"
SUPPORT_PHONE  = "+998-90-435-43-56"
