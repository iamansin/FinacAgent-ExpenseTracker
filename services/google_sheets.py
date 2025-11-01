import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import streamlit as st
from typing import Any

@st.cache_resource
def get_sheets_service():
    """Cache Google Sheets service configuration"""
    try:
        # Try Streamlit secrets first (for Streamlit Cloud)
        if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            creds = service_account.Credentials.from_service_account_info(
                st.secrets['gcp_service_account'],
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        else:
            # Local development - use file path from .env
            creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
            if not creds_path:
                raise ValueError("GOOGLE_SHEETS_CREDENTIALS not set")
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Credentials file not found: {creds_path}")
            
            creds = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        
        service: Any = build('sheets', 'v4', credentials=creds)
        return service

    except Exception as e:
        logging.exception("Error creating Google Sheets service")
        st.error(f"Failed to create Google Sheets service: {str(e)}")
        raise e