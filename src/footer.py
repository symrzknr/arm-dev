import streamlit as st

def footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #192130;
            color: #6c757d;
            text-align: center;
            padding: 10px 0;
            font-size: 12px;
        }
        </style>
        <div class="footer">
            Made with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a> | © 2025 arm-dev
        </div>
        """,
        unsafe_allow_html=True
    )
