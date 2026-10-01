"""
Snowflake Cortex Chat using OpenAI SDK
This app demonstrates using the OpenAI SDK to interact with Snowflake-hosted LLMs.
"""

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Snowflake Cortex Chat",
    page_icon="❄️",
    layout="wide"
)

# Sidebar configuration
with st.sidebar:
    st.title("❄️ Snowflake Cortex Chat")
    st.markdown("---")
    
    # Configuration inputs
    account_url = st.text_input(
        "Account URL",
        value=os.getenv("SNOWFLAKE_ACCOUNT_URL", ""),
        help="Format: https://<account-identifier>.snowflakecomputing.com/api/v2/cortex/v1",
        type="password"
    )
    
    pat_token = st.text_input(
        "PAT Token",
        value=os.getenv("SNOWFLAKE_PAT", ""),
        type="password",
        help="Your Snowflake Programmatic Access Token"
    )
    
    # Model selection
    model_options = [
        "openai-gpt-5",
        "openai-gpt-5-mini",
        "openai-gpt-5-nano",
        "openai-gpt-5-chat",
        "openai-gpt-4-1",
        "claude-sonnet-4-5",
        "claude-4-sonnet"
    ]
    
    selected_model = st.selectbox(
        "Select Model",
        model_options,
        index=0,
        help="Choose the LLM model for inference"
    )

    streaming = True
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app uses the OpenAI SDK to interact with Snowflake-hosted LLMs via 
    the Cortex Chat Completions API.
    
    **Features:**
    - Multiple model support
    - Streaming responses
    - Conversation history
    - Token usage tracking
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# Main chat interface
st.title("💬 Chat with Snowflake Cortex")
st.caption(f"Using model: **{selected_model}**")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Validate configuration
    if not account_url or not pat_token:
        st.error("⚠️ Please configure your Snowflake account URL and PAT token in the sidebar.")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Initialize OpenAI client with Snowflake endpoint
            client = OpenAI(
                api_key=pat_token,
                base_url=f"{account_url}/api/v2/cortex/v1"
            )
            
            # Prepare messages for API
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant powered by Snowflake Cortex."}
            ] + st.session_state.messages
            
            print (messages)
            response = client.chat.completions.create(
                model=selected_model,
                messages=messages, # type: ignore
                stream=True
            ) # type: ignore
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message = str(e)
            st.error(f"❌ Error: {error_message}")
            
            # Provide helpful troubleshooting
            if "401" in error_message or "Unauthorized" in error_message:
                st.warning("**Troubleshooting:** Invalid PAT token. Please generate a new one in Snowsight.")
            elif "404" in error_message:
                st.warning("**Troubleshooting:** Check your account URL format. It should be: `https://<account-identifier>.snowflakecomputing.com/api/v2/cortex/v1`")
            elif "cross-region" in error_message.lower():
                st.warning("""
                **Troubleshooting:** This model requires cross-region inference. Enable it with:
                ```sql
                ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AZURE_US';
                ```
                """)
            else:
                st.warning("**Troubleshooting:** Check the Snowflake documentation for model availability in your region.")

# Display statistics in sidebar
if st.session_state.messages:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Chat Statistics")
        st.metric("Messages", len(st.session_state.messages))
        st.metric("Total Tokens", st.session_state.total_tokens)
