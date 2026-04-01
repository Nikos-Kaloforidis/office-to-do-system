import streamlit as st

def render_header(user_data, department_data):
    # Background styling for the bar
    st.markdown(
        """
        <style>
        .header-bar {
            background-color: #1E3A8A;
            padding: 15px 25px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }
        .user-text {
            color: white;
            font-size: 1.2rem;
            font-weight: 600;
        }
        .dept-badge {
            background-color: #3B82F6;
            color: white;
            padding: 2px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            margin-left: 10px;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    with st.container():
        # HTML portion for the colored background and text
        st.markdown(
            f"""
            <div class="header-bar">
                <div class="user-text">
                    {user_data['firstName']} {user_data['lastName']}
                    <span class="dept-badge">{department_data['name']}</span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Action Buttons positioned right below the bar for clarity
        col_nav1, col_nav2, col_spacer, col_logout = st.columns([1.5, 1.5, 4, 1])
        
        with col_nav1:
            if st.button("Create Task", use_container_width=True, key="header_create"):
                st.switch_page("pages/1_Create_New_Task.py")
                
        with col_nav2:
            if st.button("View My Tasks", use_container_width=True, key="header_view"):
                st.switch_page("pages/2_My_Tasks.py")
                
        with col_logout:
            if st.button("Logout", type="primary", use_container_width=True, key="header_logout"):
                st.session_state.client.logout()
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)