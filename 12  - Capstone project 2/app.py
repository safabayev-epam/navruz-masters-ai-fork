import gradio as gr
from jira import JIRAError
from config import COMPANY_NAME, SUPPORT_EMAIL, SUPPORT_PHONE
from qa_bot import answer_question
from ticketing import create_jira_ticket

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


def process_message(user_message, state):
    history = state['history']
    ticket_mode = state['ticket_mode']
    ticket_data = state['ticket_data']
    new_history = history.copy()
    msg = user_message.strip()

    # ── Q&A MODE ───────────────────────────────────────────────────────────
    if not ticket_mode:
        result = answer_question(msg, history)
        sources = result.get('source_documents', [])
        answer_text = result.get('answer', '').strip()

        if not sources:
            ticket_data = {'stage': 0, 'trigger': msg}
            bot = (
                "I’m sorry, I couldn’t find an answer in our documents. "
                "Would you like to create a support ticket? (yes/no)"
            )
            new_history.append({'role': 'user', 'content': msg})
            new_history.append({'role': 'assistant', 'content': bot})
            return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

        # build citation
        cites = []
        for doc in sources:
            src = doc.metadata.get('source', 'Unknown')
            pg = doc.metadata.get('page')
            cites.append(f"{src}" + (f" (p.{pg})" if pg else ""))
        citation = "**📖 Source:** " + ", ".join(sorted(set(cites)))
        full_ans = f"{answer_text}\n\n{citation}"

        new_history.append({'role': 'user', 'content': msg})
        new_history.append({'role': 'assistant', 'content': full_ans})
        return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}

    # ── TICKET FLOW ────────────────────────────────────────────────────────
    stage = ticket_data.get('stage', 0)
    low = msg.lower()

    if stage == 0:
        if low in ('yes', 'y'):
            bot = "Great! What's your name?";
            ticket_data['stage'] = 1
        else:
            bot = "No problem. Let me know if you have any other questions."
            new_history.append({'role': 'user', 'content': msg})
            new_history.append({'role': 'assistant', 'content': bot})
            return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}
        new_history.append({'role': 'user', 'content': msg})
        new_history.append({'role': 'assistant', 'content': bot})
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    if stage == 1:
        ticket_data['name'] = msg;
        ticket_data['stage'] = 2
        bot = "Thanks! What's your email address?"
        new_history.append({'role': 'user', 'content': msg})
        new_history.append({'role': 'assistant', 'content': bot})
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    if stage == 2:
        ticket_data['email'] = msg;
        ticket_data['stage'] = 3
        bot = "Please provide a brief title for the issue."
        new_history.append({'role': 'user', 'content': msg})
        new_history.append({'role': 'assistant', 'content': bot})
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    if stage == 3:
        ticket_data['title'] = msg;
        ticket_data['stage'] = 4
        bot = "Now, please describe the issue in detail."
        new_history.append({'role': 'user', 'content': msg})
        new_history.append({'role': 'assistant', 'content': bot})
        return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

    if stage == 4:
        if not msg:
            bot = "Please describe the issue in detail."
            new_history.append({'role': 'user', 'content': msg})
            new_history.append({'role': 'assistant', 'content': bot})
            return new_history, {'history': new_history, 'ticket_mode': True, 'ticket_data': ticket_data}

        full_desc = (
            f"*Original question:* {ticket_data['trigger']}\n\n"
            f"*User description:* {msg}"
        )
        try:
            issue = create_jira_ticket(
                ticket_data['name'],
                ticket_data['email'],
                ticket_data['title'],
                full_desc
            )
            bot = f"Your support ticket has been created: **{issue}**."
        except JIRAError as e:
            bot = f"Failed to create ticket: {e.status_code} {e.text}"

        new_history.append({'role': 'user', 'content': msg})
        new_history.append({'role': 'assistant', 'content': bot})
        return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}

    # fallback
    bot = "Sorry, I didn't understand that."
    new_history.append({'role': 'user', 'content': msg})
    new_history.append({'role': 'assistant', 'content': bot})
    return new_history, {'history': new_history, 'ticket_mode': False, 'ticket_data': {}}


def send_message(user_message, state):
    chat, new_state = process_message(user_message, state)
    return chat, new_state, ""  # clear input


with gr.Blocks(css=css) as demo:
    gr.HTML(f"<h1 id='title'>🛠 {COMPANY_NAME} Support Chatbot</h1>")
    gr.HTML(f"<h3 id='subtitle'>Contact: <a href='mailto:{SUPPORT_EMAIL}'>{SUPPORT_EMAIL}</a> | {SUPPORT_PHONE}</h3>")

    chatbot = gr.Chatbot(type="tuples", elem_id="chatbot")
    user_input = gr.Textbox(placeholder="Type your message...", show_label=False, elem_id="input-box")
    send_btn = gr.Button("Send")
    state = gr.State({'history': [], 'ticket_mode': False, 'ticket_data': {}})

    user_input.submit(fn=send_message, inputs=[user_input, state], outputs=[chatbot, state, user_input], queue=True)
    send_btn.click(fn=send_message, inputs=[user_input, state], outputs=[chatbot, state, user_input], queue=True)

if __name__ == "__main__":
    demo.launch()
