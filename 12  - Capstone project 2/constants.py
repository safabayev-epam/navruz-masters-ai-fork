# constants.py

CSS = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
  flex-shrink: 0; 
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%; 
  padding: 0 1.5rem;
  color: #fff;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

/* Classes for aligning elements under a chat message */
.chat-sub-item-wrapper {
    margin-bottom: 1rem;
}
.chat-sub-item-content {
    box-sizing: border-box;
}
</style>
'''

BOT_TEMPLATE = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/1shjLH8/chat-bot.jpg" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

USER_TEMPLATE = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/D8gZPkX/f1624829-f27e-4d21-b691-43cff60c0539.jpg" alt="User Avatar">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

JIRA_URL = "https://knowledgeassist.atlassian.net"
JIRA_USERNAME = "navruzbek_safoboev@student.itpu.uz"
JIRA_PROJECT_KEY = "KAN"

STRICT_PROMPT = """
You are a helpful assistant. Answer the user's question using ONLY the provided context from the document(s) below.
If the answer cannot be found in the context, just say "I don't know" or "The answer is not in the provided document(s).".
Do not use any outside knowledge.

Context:
{context}

Question: {question}
Helpful answer:
"""

# Predefined list of "not found" messages for robust checking
NOT_FOUND_MESSAGES = [
    "I don't know",
    "I don't know.",
    "The answer is not in the provided document(s)",
    "The answer is not in the provided document(s)."
]
