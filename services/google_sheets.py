import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
import tempfile
import streamlit as st
from typing import Any

@st.cache_resource
def get_sheets_service():
    """Cache Google Sheets service configuration"""
    try:
        creds_env = os.getenv('GOOGLE_SHEETS_CREDENTIALS')

        # If the env variable points to a file path (local dev)
        if creds_env and os.path.exists(creds_env):
            creds = service_account.Credentials.from_service_account_file(
                creds_env,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        else:
            # On Streamlit Cloud, the env variable will contain the JSON string itself
            creds_json = json.loads(creds_env)

            # Create a temporary file for Google API
            with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp:
                json.dump(creds_json, temp)
                temp.flush()
                temp_path = temp.name

            creds = service_account.Credentials.from_service_account_file(
                temp_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )

        service: Any = build('sheets', 'v4', credentials=creds)
        return service

    except Exception as e:
        logging.exception("Error creating Google Sheets service")
        raise e
