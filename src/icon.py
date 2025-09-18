from streamlit_lottie import st_lottie
import streamlit as st
import requests
import base64
import urllib.parse
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

    Parameters:
    - label (str): Left-side text (or only text if message=None)
    - message (str): Optional right-side text
    - color (str): Badge background color (hex or name). If None, uses brand color
    - style (str): Badge style ('plastic', 'flat', 'flat-square', 'for-the-badge', 'social')
    - logo (str): SimpleIcons logo name (e.g., 'python', 'mongodb')
    - logoColor (str): Logo color
    - labelColor (str): Background color of label part
    - width (int/float): Width of the badge in pixels (optional, scaling only)
    - height (int/float): Height of the badge in pixels (optional, scaling only)
    - border_color (str): Hex or named color for border around badge
    - border_radius (int/float): Rounded corners in pixels (optional)

    Returns:
    - str: Full Shields.io badge URL
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
    # url += "&logoWidth=30"

    # Render in Streamlit with optional width, height, border, and border-radius
    html_style = ""
    if border_color or width or height or border_radius:
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
        st.markdown(f'<div style="display:inline-block; background:#{background_color}; border-radius:8px; padding:12px;"><img src="{url}" style="{html_style}"></div>', unsafe_allow_html=True)
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