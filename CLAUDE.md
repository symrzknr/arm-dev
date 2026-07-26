# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal portfolio/CV web app built with Streamlit. It displays career history, tech stack badges, project listings (professional, freelance, personal), an interactive career timeline chart, and a contact form that sends email via SMTP.

## Running the app

**Locally:**
```bash
pip install -r requirements.txt   # streamlit, pandas, streamlit-lottie, requests, plotly
streamlit run main.py
```

**With Docker (dev mode with live reload):**
```bash
docker-compose -f docker-compose.dev.yml up
```
App runs on `http://localhost:8501`. Docker uses Python 3.13-slim.

No tests or linter configured.

## Secrets

Email functionality requires `.streamlit/secrets.toml` with:
```toml
smtp_server = "..."
smtp_port = 587
email_user = "..."
email_pass = "..."
email_destination = "..."
```
This file already exists but is gitignored.

## Architecture

`main.py` is the single entry point. It defines four page functions and wires them into Streamlit's multi-page navigation:
- `page_main` — "About me" page with hero section, tech stack badges, career timeline heatmap, and contact form
- `page_prof_projects` / `page_freelance_projects` / `page_pers_projects` — project listing pages

**`src/` modules:**
- `projects_data.py` — loads all three `projects*.json` files into a single concatenated DataFrame used for the heatmap
- `project_render.py` — `project(p)` renders a single project card (name, objective, role, badges, tech icons)
- `plotly_plots.py` — `get_heatmap_data(df, x, y, color)` builds the interactive scatter+bar subplot figure
- `icon.py` — `shields_badge()` renders tech stack badges via Shields.io (with local PNG fallbacks in `src/media/fallback/` for logos Shields.io doesn't support); `st_link_button()` renders icon-wrapped anchor tags; `get_lottie_icon()` fetches Lottie animations from remote URLs
- `email_send.py` — two-step email flow using `st.session_state` flags: `send_email()` sets `show_dialog=True` and reruns, `send_dialog()` is a `@st.dialog` that sets `confirmed_send`, and `smtp_send()` does the actual SMTP send. Form fields reset via `reset_form` session flag in `main.py`
- `business_badges.py` — lookup dict mapping business field names (e.g. "Risk", "Dashboard") to Material icon strings used in project cards
- `style.py` — injects Google Fonts (Roboto) and devicon CSS globally at import time (imported as a side-effect in `main.py`: `import src.style as style`)
- `text.py` — small helper for rendering sized text via `unsafe_allow_html` markdown
- `footer.py` — renders a fixed-position footer via `st.markdown`

**Data files** (`src/*.json`): `projects.json`, `projects_freelance.json`, `projects_personal.json`. Each is a dict keyed `"1"`, `"2"`, … Each project object has fields: `name`, `icon`, `objective`, `role`, `sector`, `year`, `month`, `dates` (list), `business` (description), `business_fields` (list), `technologies` (list), `company`.

**Static assets:** `src/media/` contains profile images, social icons, and `src/media/fallback/` has local PNGs for tech badges not available on Shields.io. The `local_icons` dict in `icon.py` maps tech names to these fallback paths.

**Theme:** Configured in `.streamlit/config.toml` — dark base, `#FF4B4B` primary, `#192130` background. Orange (`color:orange`) is used extensively in inline HTML styles throughout `main.py`. All Plotly plot backgrounds use `#192130` to match.
