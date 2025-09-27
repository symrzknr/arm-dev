import streamlit as st

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<link rel="stylesheet" type='text/css' href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css" />  
    """,
    unsafe_allow_html=True
)


icons = {
    'python': """<i class="devicon-python-plain" style="font-size: 20px; color: white;"></i>""",
}

