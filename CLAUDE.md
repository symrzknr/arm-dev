# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal portfolio/CV web app built with Streamlit. It displays career history, tech stack badges, project listings (professional, freelance, personal), an interactive career timeline chart, and a contact form that sends email via SMTP.

## Running the app

**Locally:**
```bash
streamlit run main.py
```

**With Docker (dev mode with live reload):**
```bash
docker-compose -f docker-compose.dev.yml up
```
App runs on `http://localhost:8501`.

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
- `icon.py` — `shields_badge()` renders tech stack badges via Shields.io (with local PNG fallbacks for logos Shields.io doesn't support); `st_link_button()` renders icon-wrapped anchor tags; `get_lottie_icon()` fetches and plays Lottie animations
- `email_send.py` — two-step email flow: `send_email()` triggers a confirmation dialog, `smtp_send()` does the actual SMTP send using `st.secrets`
- `business_badges.py` — lookup dict mapping business field names (e.g. "Risk", "Dashboard") to Material icon strings used in project cards
- `style.py` — injects Google Fonts (Roboto) and devicon CSS globally at import time (imported as a side-effect in `main.py`)
- `footer.py` — renders a fixed-position footer via `st.markdown`

**Data files** (`src/*.json`): `projects.json`, `projects_freelance.json`, `projects_personal.json`. Each is a dict keyed `"1"`, `"2"`, … Each project object has fields: `name`, `icon`, `objective`, `role`, `sector`, `year`, `month`, `dates` (list), `business` (description), `business_fields` (list), `technologies` (list), `company`.

**Theme:** Configured in `.streamlit/config.toml` — dark base, `#192130` background, orange primary. All custom plot backgrounds use `#192130` to match.
