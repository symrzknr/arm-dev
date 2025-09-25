import streamlit as st
from src.icon import shields_badge
import copy
from random import randrange
from src.business_badges import badges

colors = ["red", "green", "yellow", "blue", "orange", "violet", "gray"]

def project(p):

    colors_copy_project = copy.deepcopy(colors)
    
    c1,c2, c3 = st.columns([12,1,24])
    with c1:
        st.subheader(p["icon"] + " " + p["name"])
        st.write(p["objective"])
        st.caption(p["role"] + ", :orange[" + ' - '.join(p["sector"])+ "]")
        st.caption(p["year"]+ "/" + p["month"])
        with st.container(
                horizontal = True,
                gap = "small",                
                horizontal_alignment = "right",                
                ):
            for i,b in enumerate(p["business_fields"]):

                if i == 0: colors_copy = copy.deepcopy(colors_copy_project)
                
                badge_color = colors_copy[randrange((len(colors_copy)-1))]
                
                st.badge(
                      label = b,
                      icon = badges[b]["icon"],
                      color = colors_copy.pop(colors_copy.index(badge_color)),
                      width = "stretch",
                 )
    with c3:
        
        st.markdown('<p style="font-size:16px;">' + p["business"] + '</p>', unsafe_allow_html= True)
        with st.container(
                horizontal = True,
                gap = "small",                
                horizontal_alignment = "distribute",                
                ):

            for tech in p["technologies"]:
                        shields_badge(
                            tech,
                            logo=tech,
                            width=None,
                            height=22,
                            border_color="a3a3a3",
                            border_radius = 14,
                            background_color = "161C26",
                        )

    st.divider()