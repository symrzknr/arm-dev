from streamlit_lottie import st_lottie
import streamlit as st
import requests
import base64
import urllib.parse
from pathlib import Path

local_icons = {
    "openai": "./src/media/fallback/chatgpt.png",
    "aws": "./src/media/fallback/aws.png",
    "powerbi": "./src/media/fallback/powerbi.png",
    "scikit": "./src/media/fallback/scikit.png",
    "heroku": "./src/media/fallback/heroku.png",
    "office": "./src/media/fallback/office.png",
    "sharepoint": "./src/media/fallback/sharepoint.png",
    "airflow": "./src/media/fallback/airflow.png",
    "tweepy": "./src/media/fallback/tweepy.png",
    "vscode": "./src/media/fallback/vscode.png",
    "pyspark": "./src/media/fallback/pyspark.png",
    "sql": "./src/media/fallback/sql.png",
}
#FFA500
# https://github.com/inttter/md-badges?utm_source=chatgpt.com

icons_url = {
    'bar_chart': "https://lottie.host/994cd218-0f36-430f-90af-b7f36f6cd84b/bJMQpyi6fV.json",
    'linkedin': "./src/media/linkedin.png",
}

def shields_badge(text, color="161C26", style="flat-square",
                  logo=None, logoColor=None, labelColor=None,
                  width=None, height=None, border_color=None, border_radius=None, background_color = None):
    """
    Generate a Shields.io badge URL with official brand colors by default.
    Falls back to local PNG if Shields.io logo is not found.
    """

    base = "https://img.shields.io/badge/"

    # Encode the text for URL
    text_enc = urllib.parse.quote(text)

    # Empty label "-" to preserve literal text
    url = f"{base}-{text_enc}-{color}?style={style}"

    if logo:
        url += f"&logo={logo}"
    if logoColor:
        url += f"&logoColor={logoColor}"
    if background_color:
        url += f"&color={background_color}"

    # Prepare HTML style
    html_style = ""
    style_list = []
    if width:
        style_list.append(f"width:{width}px;")
    if height:
        style_list.append(f"height:{height}px;")
    if border_color:
        style_list.append(f"border:2px solid {border_color};")
    if border_radius:
        style_list.append(f"border-radius:{border_radius}px;")
    html_style = " ".join(style_list)

    # Try local fallback if logo is in our dictionary
    if logo and logo.lower() in local_icons:
        png_path = local_icons[logo.lower()]
        if Path(png_path).exists():
            icon_base64 = get_base64_of_bin_file(png_path)
            

            st.markdown(
                f'<div style="display:inline-block; background:#{background_color or color}; border-radius:8px; padding:12px;">'
                f'<img src="data:image/png;base64,{icon_base64}" style="height:18px; width:auto; vertical-align:middle;">'
                f'<p style="display:inline-block; color:#fff; margin-left:8px; font-size:11px; font-weight: 400; height: 4px;">{logo}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            return f"local:{logo}"

    # Render normal Shields.io badge
    if border_color or width or height or border_radius:
        st.markdown(
            f'<div style="display:inline-block; background:#{background_color or color}; border-radius:8px; padding:12px;">'
            f'<img src="{url}"'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.image(url)

    return url


def get_lottie_icon(name, w, h):
    lottie_json = requests.get(icons_url[name]).json()
    return st_lottie(lottie_json, speed=1, loop=False, width=w, height=h)

def get_dir_icon(name):
    return icons_url[name]

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def st_link_button(url, icon_path, width=20):
    icon_base64 = get_base64_of_bin_file(icon_path)
    st.markdown(
        f"""
        <a href="{url}" target="_blank" style="
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            width:{width}px;
            height:{width}px;
            border: 2px solid orange;
            border-radius: 50%;
        ">
            <img src="data:image/png;base64,{icon_base64}" width="{int(width*0.6)}" style="display:block;">
        </a>
        """,
        unsafe_allow_html=True
    )