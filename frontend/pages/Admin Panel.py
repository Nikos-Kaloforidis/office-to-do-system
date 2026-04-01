import streamlit as st
from utils.api_client import client
from Home import render_task_card
from datetime import datetime
st.set_page_config(page_title="Admin Control", layout="wide")

if st.session_state.get("logged_in"):
    if st.session_state.get("username") == "admin":
        dept_data = client.get("api/department/show/all")
        dept_list = dept_data.get("departments", [])
        user_data = client.get("api/users/show/all")
        user_list = user_data.get("users", [])

        st.title("Admin Dashboard")

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Departments", len(dept_list))
        m2.metric("Total Users", len(user_list))
        m3.metric("System Status", "Active", delta="Normal")

        st.divider()

        # --- 3. Interactive Department Table ---
        st.subheader("Manage Departments")
        col1, col2, col3 = st.columns([1, 1, 3]) 
        if "show_add_form" not in st.session_state:
            st.session_state.show_add_form = False

        if "show_del_form" not in st.session_state: 
            st.session_state.show_del_form = False
        col1, col2, _ = st.columns([1, 1, 3])

        with col1:
            # Clicking this button just flips the toggle
            if st.button("Add Department", use_container_width=True, type="primary"):
                st.session_state.show_add_form = not st.session_state.show_add_form
        with col2: 
            if st.button("Delete Department",use_container_width=True, type="primary"):
                        st.session_state.show_del_form = not st.session_state.show_del_form

        # 2. Show the form OUTSIDE the button's 'if' block based on the toggle
        if st.session_state.show_add_form:
            with st.form("add_dept_form", clear_on_submit=True):
                st.write("### Create New Department")
                dept_name = st.text_input("Department Name")
                domain = st.selectbox("Domain", options=["HR", "Finance", "Support", "Developers"])
                
                submit = st.form_submit_button("Submit")
                
                if submit:
                    if dept_name:
                        data = {"name": dept_name, "domain": domain}
                        try:
                            client.post("api/department/add", data)
                            st.success("Department Created!")
                            # Reset the toggle so the form closes
                            st.session_state.show_add_form = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Please enter a name.")

        if st.session_state.show_del_form:
            with st.form("Delete Department",clear_on_submit=True):
                department_name = st.selectbox("Department", [dep["name"] for dep in  dept_list])
                if st.form_submit_button("Delete"): 
                    for dep in dept_list:
                        if department_name == dep["name"]: 
                            try:
                                client.delete(f"api/department/remove/{dep["dep_id"]}")
                                st.session_state.show_del_form = False 
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")

                            



        if not dept_list:
            st.warning("No departments found.")
        else:
            # 2. Loop through each department and create an expander
            for dept in dept_list:
                d_id = dept["dep_id"]
                d_name = dept["name"]
                d_domain = dept["domain"]

                # 3. Create the Expander
                # The label shows the Dept Name and Domain for quick info
                with st.expander(f"📁 {d_name} ({d_domain})"):
                    
                    # 4. Filter users belonging to THIS department
                    dept_users = [u for u in user_list if u.get("dep_id") == d_id]

                    if dept_users:
                        # Create a mini-header for the user list
                        st.markdown("#### Assigned Personnel")
                        
                        # Use columns for a clean "User Card" look inside the expander
                        for user in dept_users:
                            col_icon, col_info, col_action = st.columns([0.1, 0.7, 0.2])
                            
                            with col_icon:
                                st.write("👤")
                            
                            with col_info:
                                st.write(f"**{user['firstName']} {user['lastName']}**")
                                st.caption(f"Username: {user['username']}")
                            
                            with col_action:
                                with st.popover("Manage"):
                                    st.markdown(f"**Settings for {user['username']}**")
                                    
                                    # --- Password Update Section ---
                                    new_pwd = st.text_input("New Password", type="password", key=f"pwd_{user['user_id']}")
                                    if st.button("Update Password", key=f"upd_{user['user_id']}", use_container_width=True):
                                        if new_pwd:
                                            try:
                                                client.patch(f"api/users/update/password/{user['user_id']}", {"password": new_pwd})
                                                st.success("Password changed!")
                                            except Exception as e:
                                                st.error(f"Error: {e}")
                                        else:
                                            st.warning("Enter a password first.")

                                    st.divider()

                                    # --- Delete Section ---
                                    if st.button("Delete User", key=f"del_{user['user_id']}", type="primary", use_container_width=True):
                                        try:
                                            client.delete(f"api/users/remove/{user['user_id']}")
                                            st.toast(f"User {user['username']} deleted.")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Delete failed: {e}")

                            st.divider()
                    else:
                        st.info("No users assigned to this department yet.")

        st.markdown("## Create User")
        with st.form("User Add", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                firstName = st.text_input("First Name")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
            with col2:
                lastName = st.text_input("Last Name")
                dept_options = {dep["name"]: dep["dep_id"] for dep in dept_list}
                selected_dept = st.selectbox("Department", options=list(dept_options.keys()))
                re_enter_password = st.text_input("Confirm Password", type="password")

            submit = st.form_submit_button("Create User", type="primary")

            if submit:
                if not firstName or not username or not password:
                    st.error("All fields are required.")
                elif password != re_enter_password:
                    st.error("Passwords do not match!")
                else:
                    user_payload = { 
                        "firstName": firstName,
                        "lastName": lastName,
                        "username": username,
                        "password": password,
                        "dep_id": dept_options[selected_dept]
                    }
                    
                    try:
                        client.post("api/users/create/", user_payload)
                        st.success(f"User '{username}' added.")
                        st.balloons()
                    except Exception as e: 
                        st.error(f"Error: {e}")

        st.subheader("System-Wide Tasks")

        # 1. Hit the 'Get All' endpoint
        all_tasks_res = client.get("api/tasks/")

        # 2. Safety check: Handle both a direct List and a Dictionary response
        if isinstance(all_tasks_res, list):
            all_tasks = all_tasks_res
        elif isinstance(all_tasks_res, dict):
            # Fallback if your backend still wraps the list in a "tasks" key
            all_tasks = all_tasks_res.get("tasks", [])
        else:
            all_tasks = []

        # 3. Use the same Tab logic as before
        t_all, t_req, t_work, t_done = st.tabs(["All", "Requested", "Working", "Completed"])

        tab_map = {
            t_all: "all",
            t_req: "requested",
            t_work: "working",
            t_done: "completed"
        }

        for tab, filter_val in tab_map.items():
            with tab:
                filtered = [t for t in all_tasks if filter_val == "all" or t['status'].lower() == filter_val]
                
                if not filtered:
                    st.info(f"No tasks found for status: {filter_val.capitalize()}")
                else:
                    cols = st.columns(2)
                    for i, task in enumerate(filtered):
                        with cols[i % 2]:
                            # Prefix 'admin' to keep keys unique from any other task lists on page
                            render_task_card(task, prefix=f"admin_{filter_val}")
    else: 
        st.error("Only admin can see this page")
else:
    st.error("You need to login in order to see that page")