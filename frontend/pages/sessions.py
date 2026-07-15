import streamlit as st
import pandas as pd

from utils.session_state import initialize_session_state, set_session_id
from services.api_client import list_sessions


st.set_page_config(
    page_title="Manage Sessions",
    page_icon="💬",
    layout="wide"
)


# Initialize
initialize_session_state()


st.title("💬 Session Manager")
st.markdown("View and manage your chat sessions")

st.divider()


try:
    # Fetch sessions
    sessions_response = list_sessions()
    sessions = sessions_response.get("sessions", [])
    
    if sessions:
        st.subheader(f"Total Sessions: {len(sessions)}")
        
        # Convert to DataFrame for better display
        df_data = []
        for session in sessions:
            df_data.append({
                "Session ID": session["session_id"][:12] + "...",
                "Full ID": session["session_id"],
                "Namespace": session.get("active_namespace", "N/A"),
                "Messages": session.get("message_count", 0),
                "Created": session.get("created_at", "N/A")
            })
        
        df = pd.DataFrame(df_data)
        
        # Display sessions table
        st.dataframe(
            df[["Session ID", "Namespace", "Messages", "Created"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        # Session selection
        st.subheader("🔄 Load Session")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_idx = st.selectbox(
                "Select a session to load:",
                range(len(df)),
                format_func=lambda i: f"{df.iloc[i]['Namespace']} - {df.iloc[i]['Session ID']}"
            )
        
        with col2:
            if st.button("Load", use_container_width=True):
                session_id = df.iloc[selected_idx]["Full ID"]
                set_session_id(session_id)
                st.session_state.messages = []
                st.success("Session loaded!")
                st.switch_page("app.py")
    
    else:
        st.info("No sessions found. Create one in the chat!")

except Exception as error:
    st.error(f"Error loading sessions: {error}")
