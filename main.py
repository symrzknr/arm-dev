import streamlit as st
import pandas as pd


import json
from src.project_render import project
from src.footer import footer
import src.style as style
import src.text as text
import src.icon as icon


st.set_page_config(
    page_title="arm-dev",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def page_main():
    c1,c2,c3 = st.columns([1,7,1])
    with c2:
        with st.container(
            border = False,
        ):
            sc1, sc2, sc3 = st.columns([5,1,1])
            with sc1:
                sc11, sc18 = st.columns([1,5])
                with sc11:
                    icon.get_lottie_icon("bar_chart", 100, 100)
                    
                with sc18:
                    with st.container(vertical_alignment = "bottom"):
                        st.write(" ")
                        st.write(" ")
                        st.markdown(
                            """
                            <p style="font-size:40px;">
                                Hello, I'm <span style="color:orange;">@arm</span>
                            </p>
                            """,
                            unsafe_allow_html=True
                        )
            with sc2:
                with st.container(
                    border = False,
                    horizontal_alignment = 'right',
                    vertical_alignment = 'center',
                ):
                    st.image("./src/media/FotoCB.png", width = 100)
                
            with sc3: 
                with st.container(
                    horizontal = False,
                ):
                    icon.st_link_button("https://github.com", "./src/media/linkedin.png", width=36)
                    icon.st_link_button("https://github.com", "./src/media/sobre.png", width=36)
                

            st.markdown(
                    """
                    <p style="font-size:18px;">
                        👋 Hey there! I'm Mario, a dedicated engineer, with a primary focus on <span style="color:orange;">technology</span> and <span style="color:orange;">data</span>. During my studies in engineering and mathematics, I discovered that my real passion was <span style="color:orange;">coding</span>.
                    </p>
                    <p style="font-size:18px;">
                        I have +8 years of professional experience in <span style="color:orange;">business intelligence</span> and <span style="color:orange;">automation</span> projects in international environments, translating business requirements into analytical solutions and strategies.
                    </p>
                    <p style="font-size:18px;">
                        I'm currently working in Santander Group bank, where I perform as a senior risk data analyst focusing on data strategy.
                    </p>
                    <p style="font-size:18px;">
                        Here are some of the technologies I like to work with:
                    </p>
                    </br>
                    """,
                    unsafe_allow_html=True
                )
            
            # Custom size and border
            with st.container(
                horizontal = True,
                gap = "medium",                
                horizontal_alignment = "right",                
                ):
                tech_list = ['python', 'django', 'streamlit', 'pandas', 'plotly', 'dash', 'mysql', 'mongodb', 'postgresql', 'airflow', 'powerbi', 'aws', 'docker', 'openai', 'javascript', 'github', 'postman', 'jira']
                for tech in tech_list:
                    icon.shields_badge(
                        tech,
                        logo=tech,
                        width=None,
                        height=28,
                        border_color="a3a3a3",
                        border_radius = 14,
                        background_color = "161C26",
                    )
            
            

def page_prof_projects():
    
    
    with open("./src/projects.json", "r") as file:
        data = json.load(file)
    st.divider()
    c1,c2,c3 = st.columns([1,7,1])
    with c2:
        for i,proj in enumerate(data):
            project(data[str(i+1)])

    st.caption("The project descriptions provided on this page are intentionally kept at a high level to protect sensitive information. Specific details, data, and proprietary methods are subject to professional Non-Disclosure Agreements (NDAs) and cannot be publicly shared. The summaries are intended solely to illustrate the nature of my work and experience without disclosing confidential or privileged material.")

def page_pers_projects():
    st.write("")

footer()

pages = {
    "About me": [
        st.Page(page_main, title="arm", icon = ":material/person:"),
    ],
    "Projects": [
        st.Page(page_prof_projects, title="Professional", icon = ":material/rocket_launch:"),
        st.Page(page_pers_projects, title="Personal", icon = ":material/interests:"),
    ],
}
pg = st.navigation(pages, position = "sidebar")

pg.run()

