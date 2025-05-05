import os
import re
import gradio as gr
from jira import JIRA, JIRAError
from config import (
    COMPANY_NAME, SUPPORT_EMAIL, SUPPORT_PHONE,
    JIRA_EMAIL, JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_PROJECT_KEY
)
from qa_bot import answer_question

# Custom CSS for full-window chat and styling
css = """
body { margin: 0; padding: 0; }
.gradio-container { width: 100vw !important; max-width: none !important; }
#title { text-align: center; margin: 0.5em 0; font-family: Arial, sans-serif; }
#subtitle { text-align: center; color: #555; margin: 0 0 1em; font-family: Arial, sans-serif; }
.gradio-chatbot {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 1em;
    height: 70vh;
    overflow-y: auto;
    font-family: Arial, sans-serif;
}
#input-row { display: flex; gap: 0.5em; margin-top: 1em; }
#input-box { flex: 1; }
"""

def create_jira_client():
    return JIRA(
        server=JIRA_SERVER_URL,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        timeout=10
    )

def create_jira_ticket(name, email, title, description):
    jira = create_jira_client()
    issue = jira.create_issue(fields={
        "project": {"key": JIRA_PROJECT_KEY},
        "summary": title,
        "description": f"*Reporter:* {name} <{email}>\n\n{description}",
        "issuetype": {"name": "Task"},
    })
    return issue.key

def process_message(user_message, state):
    history      = state['history']
    ticket_mode  = state['ticket_mode']
    ticket_data  = state['ticket_data']
    new_history  = history.copy()

    lower_msg = user_message.lower()
    # Get supported languages from PDF filenames
    data_files      = [f.lower() for f in os.listdir("data") if f.lower().endswith(".pdf")]
    available_langs = {os.path.splitext(f)[0].split("_")[-1] for f in data_files}

    # === If not in a ticket flow and no supported language mentioned, prompt ticket ===
    if not ticket_mode:
        if not any(lang in lower_msg for lang in available_langs):
            ticket_data = {'stage': 0, 'trigger': user_message.strip()}
            bot_msg = (
                "I’m sorry, I couldn’t find an answer in our documents. "
                "Would you like to create a support ticket? (yes/no)"
            )
            new_history.append((user_message, bot_msg))
            return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    # === Q&A Mode ===
    if not ticket_mode:
        result      = answer_question(user_message, history)
        sources     = result.get('source_documents', [])
        answer_text = result.get('answer', '').strip()

        # If no sources, prompt ticket creation
        if not sources:
            ticket_data = {'stage': 0, 'trigger': user_message.strip()}
            bot_msg = (
                "I’m sorry, I couldn’t find an answer in our documents. "
                "Would you like to create a support ticket? (yes/no)"
            )
            new_history.append((user_message, bot_msg))
            return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

        # Build citation line for found answers
        cites = []
        for doc in sources:
            src = doc.metadata.get('source', 'Unknown')
            pg  = doc.metadata.get('page')
            cites.append(f"{src}" + (f" (p.{pg})" if pg else ""))
        citation = "**📖 Source:** " + ", ".join(sorted(set(cites)))
        bot_msg = f"{result['answer']}\n\n{citation}"
        new_history.append((user_message, bot_msg))
        return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}

    # === Ticket Creation Flow ===
    stage = ticket_data.get('stage', 0)

    # Stage 0: confirm ticket creation
    if stage == 0:
        if lower_msg in ('yes', 'y'):
            bot_msg = "Great! What's your name?"
            ticket_data['stage'] = 1
        else:
            bot_msg = "No problem. Let me know if you have any other questions."
            new_history.append((user_message, bot_msg))
            return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}
        new_history.append((user_message, bot_msg))
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    # Stage 1: collect name
    if stage == 1:
        ticket_data['name'] = user_message.strip()
        ticket_data['stage'] = 2
        new_history.append((user_message, "Thanks! What's your email address?"))
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    # Stage 2: collect email
    if stage == 2:
        ticket_data['email'] = user_message.strip()
        ticket_data['stage'] = 3
        new_history.append((user_message, "Please provide a brief title for the issue."))
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    # Stage 3: collect title
    if stage == 3:
        ticket_data['title'] = user_message.strip()
        ticket_data['stage'] = 4
        new_history.append((user_message, "Now, please describe the issue in detail."))
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    # Stage 4: collect description & create ticket
    if stage == 4:
        desc = user_message.strip()
        if not desc:
            new_history.append((user_message, "Please describe the issue in detail."))
            return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

        full_desc = (
            f"*Original question:* {ticket_data.get('trigger')}\n\n"
            f"*User description:* {desc}"
        )
        try:
            issue_key = create_jira_ticket(
                ticket_data['name'], ticket_data['email'], ticket_data['title'], full_desc
            )
            bot_msg = f"Your support ticket has been created: **{issue_key}**. We will contact you soon."
        except JIRAError as e:
            bot_msg = f"Failed to create ticket: {e.status_code or ''} {e.text or ''}"
        new_history.append((user_message, bot_msg))
        return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}

    # Fallback
    new_history.append((user_message, "Sorry, I didn't understand that."))
    return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}

def send_message(user_message, state):
    chat, new_state = process_message(user_message, state)
    return chat, new_state, ""  # clear input

with gr.Blocks(css=css) as demo:
    gr.HTML(f"<h1 id='title'>🛠 {COMPANY_NAME} Support Chatbot</h1>")
    gr.HTML(f"<h3 id='subtitle'>Contact: <a href='mailto:{SUPPORT_EMAIL}'>{SUPPORT_EMAIL}</a> | {SUPPORT_PHONE}</h3>")

    chatbot    = gr.Chatbot(type="tuples", elem_id="chatbot")
    user_input = gr.Textbox(placeholder="Type your message...", show_label=False, elem_id="input-box")
    send_btn   = gr.Button("Send")
    state      = gr.State({'history': [], 'ticket_mode': False, 'ticket_data': {}})

    user_input.submit(fn=send_message, inputs=[user_input, state], outputs=[chatbot, state, user_input], queue=True)
    send_btn.click(fn=send_message,   inputs=[user_input, state], outputs=[chatbot, state, user_input], queue=True)

if __name__ == "__main__":
    demo.launch()
