import streamlit as st

texts = {
    'presentation':{
        'header': "Hello, i am :red[arm]",
    },
}

def get_text(s1, s2, size):

    return st.markdown(
        f"""<p style="font-size:{size}px;">{texts[s1][s2]}</p>""",
        unsafe_allow_html = True
    )