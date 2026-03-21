import streamlit as st
import pandas as pd
import json
import time
from src.project_render import project
from src.plotly_plots import get_heatmap_data
from src.projects_data import get_project_df
from src.footer import footer
import src.style as style
import src.text as text
import src.icon as icon
from src.email_send import send_email, send_dialog, smtp_send

st.set_page_config(
    page_title="arm-dev",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if st.session_state.get("reset_form", False):
    st.session_state.sender_input = ""
    st.session_state.subject_input = ""
    st.session_state.body_input = ""
    st.session_state.reset_form = False  # clear the flag

def page_main():

    df = get_project_df()
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
                    st.image("./src/media/FotoCB.png", width = 120)
                
            with sc3: 
                with st.container(
                    horizontal = False,
                ):
                    icon.st_link_button("https://www.linkedin.com/in/arm2eu", "./src/media/linkedin.png", width=36)
                    icon.st_link_button("mailto:arm2eu@gmail.com", "./src/media/sobre.png", width=36)
                

            st.markdown(
                    """
                    <p style="font-size:18px;">
                        👋 Hey there! I'm Mario, a dedicated engineer, with a primary focus on <span style="color:orange;">technology</span> and <span style="color:orange;">data science</span>. During my studies in engineering and mathematics, I discovered that my real passion was <span style="color:orange;">coding</span>.
                    </p>
                    <p style="font-size:18px;">
                        I have +8 years of professional experience in <span style="color:orange;">business intelligence</span> and <span style="color:orange;">automation</span> projects in international environments, translating business requirements into analytical solutions and strategies. I've worked in financial risk management, process optimization, and data-driven decision-making, delivering impactful results across various industries.
                    </p>
                    <p style="font-size:18px;">
                        I've led projects and teams with a strong focus on <span style="color:orange;">business alignment</span> and clear communication with senior management. My commitment, responsibility, and <span style="color:orange;">versatility</span> ensure that every initiative delivers real value, making a meaningful difference in outcomes.
                    </p>
                    """,
                    unsafe_allow_html=True
                )
            
            st.divider()
                       
            # Custom size and border
            
            st.markdown(
                    """
                    <p style="font-size:18px;">
                        <span style="color:orange;">🖥️ Tech stack</span></br>
                        Here are some of the technologies I like to work with:
                    </p>
                    </br>
                    """,
                    unsafe_allow_html=True
                )                
            tech_list = list(df.explode("technologies")["technologies"].unique())
            tech_list += ["github", "huggingface", "ollama", "claude", "githubcopilot", "aws", "vscode", "pyspark"]
            tech_list.pop(tech_list.index("php"))
            tech_categories = {
                "Languages & Core": ["python", "javascript", "sql"],
                "Data Science & AI": [
                    "pandas", "scikit", "pyspark", "openai", "huggingface", 
                    "ollama", "claude", "githubcopilot"
                ],
                "Web dev": ["plotly", "dash", "powerbi", "streamlit", "django"],
                "Databases": ["sqlite", "postgresql", "mongodb", "snowflake"],
                "Infrastructure & Cloud": ["aws", "heroku", "docker", "airflow"],
                "Tools & Collaboration": [
                    "jira", "sap", "postman", "github", "vscode", 
                    "sharepoint", "office", "telegram"
                ]
            }

            def render_category_badges(category_name):
                """Helper to render a header and a horizontal container of badges"""
                st.write(f"**{category_name}**")
                # Using horizontal container for the badges to sit side-by-side
                with st.container(horizontal=True, gap="medium", horizontal_alignment="center"):
                    for tech in tech_categories[category_name]:
                        icon.shields_badge(
                            tech,
                            logo=tech,
                            width=None,
                            height=28,
                            border_color="a3a3a3",
                            border_radius=14,
                            background_color="161C26",
                        )
                st.write(" ") # Padding

            # --- LAYOUT LOGIC ---

            # 1. Full Width: Data Science & AI (Heavy category)
            with st.container(border=True, horizontal_alignment="center"):
                render_category_badges("Data Science & AI")

            # 2. Balanced Grid: Languages, Databases, and Infrastructure (3-column)
            col1, col2, col3, col4 = st.columns(4, gap="small", border = True)

            with col1:
                render_category_badges("Languages & Core")

            with col2:
                render_category_badges("Databases")

            with col3:
                render_category_badges("Infrastructure & Cloud")

            with col4:
                render_category_badges("Web dev")
                

            with st.container(border=True, horizontal_alignment="center"):
                render_category_badges("Tools & Collaboration")

            st.write(" ")
            st.divider()

            st.markdown(
                """
                <p style="font-size:18px;">
                    <span style="color:orange;">🚀 Career Timeline</span><br>
                    These are the main projects and roles I've had in my career so far:
                </p>
                
                """,
                unsafe_allow_html=True
            )
            cc1, cc2 = st.columns([10,2])
            with cc1:
                fig_w = st.empty()
                
            with cc2:
                
                st.caption("Play with some of my projects!")
                color_opts = ['year', 'month', 'project_type', 'role', 'company', 'sector', 'technologies', 'business_fields']
                x_axis = st.selectbox('x-axis', color_opts, index = 0)
                y_axis = st.selectbox('y-axis', color_opts, index = 1)
                color = st.selectbox('color', color_opts, index = 4)

                if x_axis == y_axis or x_axis == color or y_axis == color:
                    fig_w.info("Selections must be different")
                else:
                    fig = get_heatmap_data(df, x_axis, y_axis, color)
                    fig_w.write(fig)

            sc1, sc2, sc3 = st.columns([1,1,1])
            with sc1:
                st.markdown(
                        """
                        <p style="font-size:18px;">
                            <ul>
                                <li>
                                <b>[CITD Technology, 1.5 years]</b></br> Started my career performing stress calculus for european aerospace industry, developing a strong foundation in precision engineering and analytical thinking.
                                </li>
                            </ul>
                        </p>
                        </br>
                        """,
                        unsafe_allow_html=True
                    )
            with sc2:
                st.markdown(
                        """
                        <p style="font-size:18px;">
                            <ul>
                                <li>
                                <b>[KPMG Advisory, 5.5 years]</b></br> Then, I transitioned into consulting, where I improved my expertise in data analysis, process improvement, and business strategy, working with diverse clients and complex projects as a manager.
                                </li>
                            </ul>
                        </p>
                        
                        </br>
                        """,
                        unsafe_allow_html=True
                    )
            with sc3:
                st.markdown(
                        """
                        <p style="font-size:18px;">
                            <ul>
                                <li>
                                <b>[Santander Banking Group, 2 years]</b></br> Currently serving as a Senior Full-Stack Data Analyst, driving international data strategy initiatives and building end-to-end solutions that bridge technical implementation and business impact.
                                </li>
                            </ul>
                        </p>
                        
                        </br>
                        """,
                        unsafe_allow_html=True
                    )
            st.divider()

            c1,c2,c3 = st.columns([1,4,1])

            with c2:
                st.header("Contact")

                sc1, sc2 = st.columns([3,4])
                with sc1:
                    sender = st.text_input("Your email:red[*]", key="sender_input")
                with sc2:
                    subject = st.text_input("Subject:red[*]", key="subject_input")
                body = st.text_area("Message:red[*]", key="body_input")

                sc1, sc2 = st.columns([1,5])
                    
                send = st.button("Send", icon="✉️", use_container_width=True)

                with sc2:
                    if send:
                        msg = {"sender": sender, "subject": subject, "body": body}
                        if all([msg[k] for k in msg]):

                            send_email(msg)
                            # Show dialog if state says so
                        else:
                            st.info("Please, fill all the fields")

                    if st.session_state.show_dialog:
                        send_dialog()

                    if st.session_state.confirmed_send is True:
                        result = smtp_send()
                        if result is True:
                            st.toast("✅ Email sent successfully!")
                            time.sleep(3)
                            # --- 2️⃣ Set flag and rerun ---
                            st.session_state.reset_form = True
                            st.rerun()
                            
                        else:
                            st.toast(f"❌ Failed: {result}")
                    

def page_prof_projects():

    c1,c2,c3 = st.columns([1,7,1])
    with c2:
        
        st.header(":material/rocket_launch: Professional Projects")
        st.write("A Glimpse Into My Professional Work")
        st.divider()

        with open("./src/projects.json", "r") as file:
            data = json.load(file)

        for i,proj in enumerate(data):
            project(data[str(i+1)])

    st.caption("The project descriptions provided on this page are intentionally kept at a high level to protect sensitive information. Specific details, data, and proprietary methods are subject to professional Non-Disclosure Agreements (NDAs) and cannot be publicly shared. The summaries are intended solely to illustrate the nature of my work and experience without disclosing confidential or privileged material.")

def page_freelance_projects():

    c1,c2,c3 = st.columns([1,7,1])
    with c2:
        st.header(":material/diamond_shine: Freelance Projects")
        st.write("An Overview Of My Freelance Work")
        st.divider()

        with open("./src/projects_freelance.json", "r") as file:
            data = json.load(file)

        for i,proj in enumerate(data):
            project(data[str(i+1)])

    st.caption("The project descriptions provided on this page are intentionally kept at a high level to protect sensitive information. Specific details, data, and proprietary methods are subject to professional Non-Disclosure Agreements (NDAs) and cannot be publicly shared. The summaries are intended solely to illustrate the nature of my work and experience without disclosing confidential or privileged material.")

def page_pers_projects():
    c1,c2,c3 = st.columns([1,7,1])
    with c2:
        st.header(":material/interests: Personal Projects")
        st.write("Some stuff I liked to build")
        st.divider()

        with open("./src/projects_personal.json", "r") as file:
            data = json.load(file)

        for i,proj in enumerate(data):
            project(data[str(i+1)])

footer()

pages = {
    "About me": [
        st.Page(page_main, title="arm", icon = ":material/person:"),
    ],
    "Projects": [
        st.Page(page_prof_projects, title="Professional", icon = ":material/rocket_launch:"),
        st.Page(page_freelance_projects, title="Freelance", icon = ":material/diamond_shine:"),
        st.Page(page_pers_projects, title="Personal", icon = ":material/interests:"),
    ],
}
pg = st.navigation(pages, position = "sidebar")
pg.run()

