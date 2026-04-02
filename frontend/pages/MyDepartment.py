import streamlit as st
from Home import render_task_card
from utils.api_client import client

st.set_page_config(page_title="MyDepartment", layout="wide")

if st.session_state.get("logged_in"):
    uid = st.session_state.get("user_id")
    user_info = client.get(f"/api/users/show/{uid}")
    dept_info = client.get(f"/api/department/show/{user_info['dep_id']}")
    st.subheader(f"{dept_info["name"]} Department Tasks")

    t_all, t_req, t_work, t_done = st.tabs(["All", "Requested", "Working", "Completed"])

    tab_map = {t_all: "all", t_req: "requested", t_work: "working", t_done: "completed"}

    dep_tasks_res = client.get(f"/api/tasks/department/{user_info['dep_id']}")
    dep_all_tasks = dep_tasks_res.get("tasks", [])

    for tab, filter_val in tab_map.items():
        with tab:
            # Filter the list based on the tab's status
            filtered = [
                t
                for t in dep_all_tasks
                if filter_val == "all" or t["status"].lower() == filter_val
            ]

            if not filtered:
                st.info(f"No tasks found for status: {filter_val.capitalize()}")
            else:
                cols = st.columns(2)
                for i, task in enumerate(filtered):
                    with cols[i % 2]:
                        # Crucial: Pass the filter_val as a prefix to prevent Duplicate Key errors
                        render_task_card(task, prefix=filter_val)

else:
    st.error("You need to login in order to view this page")
