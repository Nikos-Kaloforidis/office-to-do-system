import streamlit as st 
from utils.api_client import client 
from datetime import datetime
import sys
from pathlib import Path

# Force root path for ALL pages (before any imports)
root_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(root_dir))

# --- 1. Page Configuration ---
st.set_page_config(page_title="Task Portal", page_icon="📝", layout="wide")

# --- 2. Helper Function: Task Card with Unique Keys ---
def render_task_card(task, prefix):
    task_id = task.get("task_id")
    
    with st.container(border=True):
        col_title, col_status = st.columns([3, 1])
        
        with col_title:
            st.markdown(f"### {task['name']}")
            st.caption(f"Created: {task['timestamp'][:10]}")
            
        with col_status:
            if st.session_state.get("editing_task") == task_id: 
                options = ["requested", "working", "completed"]
                current_status = task['status'].lower()
                default_idx = options.index(current_status) if current_status in options else 0
                
                new_status = st.selectbox(
                    "Update Status", 
                    options=options, 
                    index=default_idx,
                    key=f"{prefix}_sel_{task_id}", 
                    label_visibility="collapsed"
                )
                
                s1, s2 = st.columns(2)
                with s1:
                    if st.button("Save", key=f"{prefix}_sv_{task_id}", type="primary"):
                        try:
                            client.patch(f"api/tasks/{task_id}", {"status": new_status})
                            st.session_state.editing_task = None
                            st.rerun()
                        except Exception as e:
                            st.error("Update failed")
                with s2:
                    if st.button("X", key=f"{prefix}_can_{task_id}"):
                        st.session_state.editing_task = None
                        st.rerun()
            else:
                status_upper = task['status'].upper()
                if status_upper == "COMPLETED": st.success(status_upper)
                elif status_upper == "WORKING": st.warning(status_upper)
                else: st.info(status_upper)

        st.write(task['description'] or "_No description provided_")
        st.divider()

        f1, f2 = st.columns([4, 1])
        with f1:
            # --- FIX STARTS HERE ---
            creator_name = "Unknown User"
            
            # 1. First, check if the full user object is already in the task
            user_obj = task.get("created_by") 
            if isinstance(user_obj, dict):
                creator_name = f"{user_obj.get('firstName', '')} {user_obj.get('lastName', '')}"
            
            # 2. If not, only then try to fetch via ID, but check if ID exists first!
            else:
                creator_id = task.get('created_by_id')
                if creator_id is not None:
                    try:
                        user_creator_data = client.get(f"/api/users/show/{creator_id}")
                        creator_name = f"{user_creator_data.get('firstName', '')} {user_creator_data.get('lastName', '')}"
                    except Exception:
                        pass # Keep 'Unknown User' if API call fails
            
            st.caption(f"Created By: {creator_name}")

            
        with f2:
            if st.session_state.get("editing_task") != task_id:
                if st.button("Edit", key=f"{prefix}_ed_{task_id}", use_container_width=True):
                    st.session_state.editing_task = task_id
                    st.rerun()
# --- 3. Header Function ---
def render_app_header(user_data, dept_data):
    with st.container():
        c1, c2, c3, c4 = st.columns([4, 1.5, 1.5, 1])
        c1.markdown(f"## Welcome, {user_data['firstName']}!")
        c1.caption(f"Department: {dept_data['name']}")
        
        if c2.button("Refresh List", use_container_width=True, key="main_refresh"):
            st.rerun()
        
        if c4.button("Logout", type="primary", use_container_width=True, key="main_logout"):
            st.session_state.client.logout()
            st.rerun()
        st.divider()

# --- 4. Main App Logic ---
if "client" not in st.session_state:
    st.session_state.client = client

if not st.session_state.get("logged_in"):
    st.markdown("<h2 style='text-align: center;'>Member Login</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.form_submit_button("Sign In"):
            if client.login(user, pw):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")
else:
    # 1. Fetch User Data
    uid = st.session_state.get("user_id")
    user_info = client.get(f"/api/users/show/{uid}")
    dept_info = client.get(f"/api/department/show/{user_info['dep_id']}")
    
    render_app_header(user_info, dept_info)

    # 2. Task Filtering with Tabs
    st.subheader("My Tasks")
    my_tasks_res = client.get(f"/api/tasks/user/{uid}")
    all_tasks = my_tasks_res.get("tasks", [])

    t_all, t_req, t_work, t_done = st.tabs(["All", "Requested", "Working", "Completed"])
    
    tab_map = {
        t_all: "all",
        t_req: "requested",
        t_work: "working",
        t_done: "completed"
    }

    for tab, filter_val in tab_map.items():
        with tab:
            # Filter the list based on the tab's status
            filtered = [t for t in all_tasks if filter_val == "all" or t['status'].lower() == filter_val]
            
            if not filtered:
                st.info(f"No tasks found for status: {filter_val.capitalize()}")
            else:
                cols = st.columns(2)
                for i, task in enumerate(filtered):
                    with cols[i % 2]:
                        # Crucial: Pass the filter_val as a prefix to prevent Duplicate Key errors
                        render_task_card(task, prefix=filter_val)

    # 3. Task Creation Section
    st.markdown("---")
    st.subheader("Create New Task")
    
    try:
        depts_data = client.get("/api/department/show/all").get('departments', [])
        users_data = client.get("/api/users/show/all").get('users', [])
    except:
        depts_data, users_data = [], []

    with st.form("new_task_form", clear_on_submit=True):
        t_name = st.text_input("Task Name*")
        t_desc = st.text_area("Description")
        
        c1, c2 = st.columns(2)
        d_opts = {d['name']: d['dep_id'] for d in depts_data}
        u_opts = {f"{u['firstName']} {u['lastName']}": u['user_id'] for u in users_data}
        
        sel_dept = c1.selectbox("Assign Department", ["None"] + list(d_opts.keys()))
        sel_user = c2.selectbox("Assign User", ["None"] + list(u_opts.keys()))
        
        if st.form_submit_button("Create Task", type="primary"):
            if t_name:
                payload = {
                    "name": t_name,
                    "description": t_desc,
                    "status": "requested",
                    "created_by_id": uid,
                    "assigned_user_id": u_opts.get(sel_user) if sel_user != "None" else None,
                    "assigned_dep_id": d_opts.get(sel_dept) if sel_dept != "None" else None,
                    "timestamp": datetime.now().isoformat()
                }
                try:
                    client.post("api/tasks/", payload)
                    st.success("Task Created!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Task name is required.")