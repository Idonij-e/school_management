# pip install fasteners
import fasteners
import os
from main.settings import GOOGLE_PROJECT_ID, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def schedule_token_refresh():
    print('scheduler is starting')
    lock_path = os.path.join(os.path.dirname(__file__), 'lock')
    lock = fasteners.InterProcessLock(lock_path)
    
    if lock.acquire(blocking=False):
        print('lock acquired')
        try:
            SCOPES = ["https://www.googleapis.com/auth/drive"]

            """
            Shows basic usage of the Drive v3 API.
            Prints the names and ids of the first 10 files the user has access to.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    client_config = {
                        "installed": {
                            "client_id": GOOGLE_CLIENT_ID,
                            "project_id": GOOGLE_PROJECT_ID,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "client_secret": GOOGLE_CLIENT_SECRET,
                            "redirect_uris": ["http://localhost"]
                        }
                    }

                    flow = InstalledAppFlow.from_client_config(
                        client_config, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
            print('token refreshed')
        finally:
            lock.release()
            print('lock released')
