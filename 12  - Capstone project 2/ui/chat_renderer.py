# ui/chat_renderer.py

import streamlit as st
from collections import defaultdict
from langchain_core.messages import AIMessage, HumanMessage

from constants import NOT_FOUND_MESSAGES, BOT_TEMPLATE, USER_TEMPLATE
from utils.jira import create_jira_ticket
from utils.pdf_processing import get_pdf_chunks
from utils.vectorstore import get_vectorstore, get_conversation_chain

def check_if_not_found(answer_text: str) -> bool:
    stripped = answer_text.strip()
    if stripped.lower() in ["i don't know", "i don't know."]:
        return True
    if stripped in [
        "The answer is not in the provided document(s).",
        "The answer is not in the provided document(s)"
    ]:
        return True
    if stripped.lower().startswith("the answer is not in the provided document"):
        return True
    return False


def handle_userinput(user_question: str):
    if st.session_state.conversation is None:
        st.warning("Please upload and process PDFs first.")
        return

    try:
        response = st.session_state.conversation({"question": user_question})
    except Exception as e:
        st.error(f"Error during conversation: {e}")
        st.session_state.chat_history.append(HumanMessage(content=user_question))
        st.session_state.chat_history.append(AIMessage(content=f"Sorry, an error occurred: {e}"))
        if "referenced_pages" not in st.session_state:
            st.session_state.referenced_pages = []
        st.session_state.referenced_pages.append([])
        return

    history = response["chat_history"]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "referenced_pages" not in st.session_state:
        st.session_state.referenced_pages = []

    # Append the last user and bot messages
    st.session_state.chat_history.append(history[-2])
    st.session_state.chat_history.append(history[-1])

    answer_text = history[-1].content
    is_not_found = check_if_not_found(answer_text)

    if is_not_found:
        st.session_state.referenced_pages.append([])
    elif "source_documents" in response and response["source_documents"]:
        seen = set()
        sources = []
        for doc in response["source_documents"]:
            meta = getattr(doc, "metadata", {})
            pdf_name = meta.get("pdf_name", "PDF")
            page = meta.get("page", "?")
            # avoid duplicates
            if (pdf_name, page) not in seen:
                seen.add((pdf_name, page))
                sources.append(f"{pdf_name}, page {page}")
        st.session_state.referenced_pages.append(sources)
    else:
        st.session_state.referenced_pages.append([])


def render_chat():
    history = st.session_state.get("chat_history", [])
    referenced_pages_list = st.session_state.get("referenced_pages", [])

    if "jira_feedback" not in st.session_state:
        st.session_state.jira_feedback = {}

    bot_idx = 0
    for i in range(0, len(history), 2):
        if i + 1 >= len(history):
            break

        user_message = history[i]
        bot_message = history[i + 1]

        # Render user & bot messages
        st.write(USER_TEMPLATE.replace("{{MSG}}", user_message.content),
                 unsafe_allow_html=True)
        st.write(BOT_TEMPLATE.replace("{{MSG}}", bot_message.content),
                 unsafe_allow_html=True)

        current_bot_pages = referenced_pages_list[bot_idx] if bot_idx < len(referenced_pages_list) else []
        bot_text = bot_message.content
        is_not_found = check_if_not_found(bot_text)
        jira_key = f"jira_{bot_idx}_{i}"

        if current_bot_pages:
            grouped = defaultdict(list)
            for ref in current_bot_pages:
                try:
                    pdf_name, page_str = ref.rsplit(", page ", 1)
                    grouped[pdf_name].append(page_str)
                except ValueError:
                    grouped["?"].append(ref)

            refs_str = "; ".join(
                f"{pdf_name} - {', '.join(page_list)}"
                for pdf_name, page_list in grouped.items()
            )
            st.markdown(f'''
            <div class="chat-sub-item-wrapper">
                <div class="chat-sub-item-content" style="background-color:#22324c; padding:10px; border-radius:8px; color:#fff;">
                    <b>Referenced pages:</b> {refs_str}
                </div>
            </div>
            ''', unsafe_allow_html=True)

        elif is_not_found:
            if not st.session_state.jira_feedback.get(jira_key, False):
                st.markdown(f'''
                <div class="chat-sub-item-wrapper">
                    <div class="chat-sub-item-content">
                ''', unsafe_allow_html=True)

                if st.button("📝 Create Jira Ticket", key=f"jira_btn_{jira_key}"):
                    st.session_state.active_jira_request = {
                        'key': jira_key,
                        'question': user_message.content,
                    }
                    st.rerun()

                st.markdown('</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="background-color:#1e3a2e; padding:10px; border-radius:4px; color:#4ade80; margin-bottom:1rem; margin-top:1rem;">'
                    '✅ Jira ticket has been created for this question'
                    '</div>',
                    unsafe_allow_html=True
                )
        bot_idx += 1
