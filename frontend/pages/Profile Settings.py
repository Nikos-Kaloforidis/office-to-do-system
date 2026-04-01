import streamlit as st 
from utils.api_client import client

from app.auth.jwt import verify_password

st.set_page_config(page_title="Admin Control", layout="wide")

if st.session_state.get("logged_in"):
    st.header("Profile Settings")

    st.subheader("Change password")
    with st.form("CHange Password",clear_on_submit=True): 
        old_password = st.text_input("Old Password",type="password")
        new_password = st.text_input("New Password",type="password")
        re_enter_password =  st.text_input("Re Enter Password",type="password")
        if st.form_submit_button("Submit Change"):
            user_data  = client.get(f"api/users/show/{st.session_state.get("user_id")}")
            print(user_data["password"])
            if verify_password(old_password,user_data["password"]):
                if new_password == re_enter_password:

                    payload = { 
                        "id": st.session_state.get("user_id"),
                        "password": new_password
                    }
                    client.put(f"api/users/update/password/{st.session_state.get("user_id")}",payload)
                    st.success("Password updated successfully")
                    st.rerun()
                else: 
                    st.error("Passwords do not match")
            else:
                st.error("Old password is incorrect")
else:
    st.error("You need to login in order to view this page")