from time import sleep
import streamlit as st

# Login page content
def loginPage(_logger, logout, list_varieties_page):
    st.write("Please log in to continue (username `testo`, password `test`).")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if not st.session_state.get("logged_in", False):
        if st.button("Log in", type="primary"):
            if username == "test" and password == "test":
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                sleep(0.5)
                st.switch_page(list_varieties_page)
            else:
                st.error("Incorrect username or password")
        else:
            _logger.info(f"Login button not pressed yet.")
    else:
        if st.button("Log out", type="primary"):
            st.session_state.logged_in = False
            st.info("Logged out successfully!")
            _logger.info(f"Logged out successfully!")
            sleep(0.5)
            logout()