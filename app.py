from datetime import datetime
import plotly.graph_objects as go 
import streamlit as st
from streamlit_option_menu import option_menu  
import pandas as pd
import scrape
page_title="Youtube Channel Statistics"
layout = "centered"
page_icon = ":lady_beetle:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)
st.header(f"Youtube Channel Infographics")
st.text_input("Enter Channel Name",key="scrape_data")
channel= st.session_state["scrape_data"]
df = scrape.youtube_videos_dataframe(channel)
st.download_button(label="DOWNLOAD!",data=df.to_csv().encode('utf-8'),file_name=f"{channel}.csv",mime="csv/plain")

