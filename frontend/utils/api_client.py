import requests
from typing import Dict, Any
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

API_BASE = os.getenv("BACKEND_URL","http://localhost:8000")


class APIClient:
    def __init__(self):
        self.headers = {}
        self._update_headers()

    def _update_headers(self):
        """Syncs the class headers with the current Streamlit session state"""
        token = st.session_state.get("access_token")
        if token:
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    def login(self, username: str, password: str) -> bool:
        try:
            resp = requests.post(
                f"{API_BASE}/authenticate/",
                json={"username": username, "password": password},
            )

            if resp.status_code in [200, 202]:
                data = resp.json()
                # Store everything in session_state
                st.session_state.access_token = data["access_token"]
                st.session_state.user_id = data["user_id"]
                st.session_state.username = data["username"]
                st.session_state.logged_in = True

                self._update_headers()
                return True
            return False
        except Exception as e:
            st.error(f"Connection Error: {e}")
            return False

    def logout(self):
        for key in ["access_token", "user_id", "username", "logged_in"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    def get(self, endpoint: str) -> Dict[str, Any]:
        response = requests.get(f"{API_BASE}/{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        response = requests.post(
            f"{API_BASE}/{endpoint}", json=data, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def patch(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        response = requests.patch(
            f"{API_BASE}/{endpoint}", json=data, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> bool:
        response = requests.delete(f"{API_BASE}/{endpoint}", headers=self.headers)
        return response.status_code == 204

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.put(
            f"{API_BASE}/{endpoint}", json=data, headers=self.headers
        )
        response.raise_for_status()
        return response.json()


# Global client
client = APIClient()
