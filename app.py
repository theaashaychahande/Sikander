
import streamlit as st
import pandas as pd
import locale
import portfolio
import risk_engine
import visualization
import data_fetcher
import config
primary = "#00d4aa"
secondary = "#355C7D"
bg_card = "#171B26"
shadow = "0 4px 12px 0 rgba(0,0,0,0.25)"
st.set_page_config(
    page_title="Sikander - Portfolio Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(f"""
<style>
body, .stApp {{ background-color: #10131A; }}
h1.main-header {{
    font-family: 'Montserrat', 'Arial', sans-serif;
    font-size: 3rem;
    color: {primary};
    text-align: center;
    padding: 0.5rem 0 0.4rem 0;
    letter-spacing: 2.5px;
    margin-bottom: 0.5rem;
    font-weight: bold;
}}
.header-tagline {{
    font-size: 1.15rem;
    color: #9ed7cb;
    text-align: center;
    margin-bottom: 1.25rem;
}}
.sidebar-card {{
    background: #19202C;
    padding: 1.2rem 1.1rem;
    margin-bottom: 1.2rem;
    border-radius: 12px;
    box-shadow: {shadow};
}}
.sidebar-section-title {{
    color: {primary};
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: .5px;
    margin: .7rem 0 .3rem 0;
}}
.kpi-card {{
    background: {bg_card};
    border-radius: 11px;
    margin-bottom: 10px;
    padding: 1.2rem 1.1rem;
    box-shadow: {shadow};
    min-height: 90px;
    text-align: center;
}}
.metric-label {{
    font-size: 1.13rem;
    color: #b1b8cf;
    margin-bottom: 0.4em;
    letter-spacing:0.2px;
}}
.metric-main {{
    font-size: 2.2rem;
    font-weight: 700;
    color: {primary};
    letter-spacing:1.3px;
}}
.metric-delta.pos {{ color: #33EEA0; }}
.metric-delta.neg {{ color: #FF6B6B; }}
.risk-positive {{ color: #33EEA0 !important; }}
.risk-negative {{ color: #FF6B6B !important; }}
.tab-header[data-baseweb="tab"] {{
    font-size:1.13rem;
    color:{secondary};
    font-weight:600;
}}
hr {{ border: 1px solid #222945; margin: 1.4em 0 1em 0; }}
.stButton>button, .stDownloadButton>button {{
    background: {primary} !important;
    color: #171B26 !important;
    border-radius: 7px !important;
    box-shadow: {shadow};
    border:none !important;
    font-weight: bold;
    transition: box-shadow 0.2s;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    box-shadow: 0 8px 24px 0 rgba(0,0,0,0.25);
    background: #20eeba !important;
}}
</style>
""", unsafe_allow_html=True)
