import streamlit as st
from src.icon import shields_badge
import copy
from random import randrange
from src.business_badges import badges

colors = ["red", "green", "yellow", "blue", "orange", "violet", "gray"]


def _render_title(p, size):
    """Render project title, handling both emoji and :material/...: icons."""
    icon = p["icon"]
    name = p["name"]
    if icon.startswith(":material/"):
        st.markdown(f"{icon} **{name}**")
    else:
        st.markdown(
            f'<p style="font-size:{size}px; margin-bottom:2px;">{icon} <b>{name}</b></p>',
            unsafe_allow_html=True,
        )


@st.dialog("Project Details", width="large")
def project_detail(p):
    """Full project detail shown in a modal dialog."""
    colors_copy = copy.deepcopy(colors)

    _render_title(p, 24)
    st.caption(
        p["role"] + ", :orange[" + " - ".join(p["sector"]) + "] — " + p["year"] + "/" + p["month"]
    )

    st.markdown(
        '<p style="font-size:15px;">' + p["business"] + "</p>",
        unsafe_allow_html=True,
    )

    with st.container(horizontal=True, gap="small"):
        for i, b in enumerate(p["business_fields"]):
            if i == 0:
                colors_copy_inner = copy.deepcopy(colors_copy)
            badge_color = colors_copy_inner[randrange(len(colors_copy_inner) - 1)]
            st.badge(
                label=b,
                icon=badges[b]["icon"],
                color=colors_copy_inner.pop(colors_copy_inner.index(badge_color)),
            )

    with st.container(horizontal=True, gap="small", horizontal_alignment="distribute"):
        for tech in p["technologies"]:
            shields_badge(
                tech, logo=tech, width=None, height=22,
                border_color="a3a3a3", border_radius=14, background_color="161C26",
            )

    st.write(" ")
    st.write(" ")


def project_card(p, key):
    """Compact project card for grid display."""
    colors_copy_project = copy.deepcopy(colors)

    with st.container(border=True):
        _render_title(p, 17)
        if p.get("objective"):
            st.caption(p["objective"])
        st.caption(
            p["role"] + ", :orange[" + " - ".join(p["sector"]) + "] — " + p["year"] + "/" + p["month"]
        )

        with st.container(horizontal=True, gap="small"):
            for i, b in enumerate(p["business_fields"]):
                if i == 0:
                    colors_copy = copy.deepcopy(colors_copy_project)
                badge_color = colors_copy[randrange(len(colors_copy) - 1)]
                st.badge(
                    label=b,
                    icon=badges[b]["icon"],
                    color=colors_copy.pop(colors_copy.index(badge_color)),
                )

        if st.button("Details", key=key, icon=":material/open_in_new:", use_container_width=True):
            project_detail(p)


def project_grid(data, prefix):
    """Render projects as a 3-column card grid."""
    keys = [str(i + 1) for i in range(len(data))]
    for row_start in range(0, len(keys), 3):
        cols = st.columns(3)
        for j in range(3):
            if row_start + j < len(keys):
                k = keys[row_start + j]
                with cols[j]:
                    project_card(data[k], key=f"{prefix}_{k}")
