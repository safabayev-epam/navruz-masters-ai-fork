# ui/jira_renderer.py

import streamlit as st
from utils.jira import create_jira_ticket

def render_jira_form():
    if 'active_jira_request' not in st.session_state:
        return

    jira_request = st.session_state.active_jira_request
    jira_form_key_suffix = jira_request['key']
    question = jira_request['question']

    st.markdown("---")
    st.subheader("Create Jira Ticket")

    with st.form(key=f"jira_form_{jira_form_key_suffix}"):
        st.write(f"**Question:** {question}")
        email = st.text_input("Your email", key=f"email_for_{jira_form_key_suffix}")
        summary = st.text_input(
            "Ticket summary",
            value=f"Missing information: {question[:50]}...",
            key=f"summary_for_{jira_form_key_suffix}"
        )
        description = st.text_area("Describe what information should be added:",
                                   key=f"desc_for_{jira_form_key_suffix}")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Submit Ticket")
        with col2:
            cancelled = st.form_submit_button("Cancel")

        if submitted:
            if email and summary and description:
                description_full = (
                    f"User email: {email}\n\n"
                    f"Original question: {question}\n\n"
                    f"Description: {description}"
                )
                with st.spinner("Creating Jira ticket..."):
                    success, result = create_jira_ticket(summary, description_full)
                if success:
                    st.success(f"✅ Jira ticket created successfully! Issue: {result}")
                    st.session_state.jira_feedback[jira_form_key_suffix] = True
                    del st.session_state.active_jira_request
                    st.rerun()
                else:
                    st.error(f"❌ Failed to create Jira ticket: {result}")
            else:
                st.error("Please fill in all fields")
        if cancelled:
            del st.session_state.active_jira_request
            st.rerun()
