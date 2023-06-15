import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
# setting up selenium driver for webscrapping
def get_driver():
    os.environ["PATH"]+='projectyoutube/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver
# scrapping youtube channel/video page for description,video links, views, video length, uploaded period.
def scrape_videos(driver):
    videos=driver.find_elements(By.XPATH, "//a[@id='video-title-link'][@class='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media']")
    uploaded_video_details={}
    uploaded_video_details["description"]=[]
    uploaded_video_details["video_links"]=[]
    uploaded_video_details["video_length"]=[]
    uploaded_video_details["views"]=[]
    uploaded_video_details["date_of_upload"]=[]
    for video in videos:
        uploaded_video_details["description"].append(video.text)
        uploaded_video_details["video_links"].append(video.get_attribute("href"))
        aria_label=video.get_attribute("aria-label").strip().split()
        views=aria_label[-2]
        video_length=aria_label[-6]+" "+aria_label[-5]+" "+aria_label[-4]+" "+aria_label[-3]
        uploaded_period=aria_label[-9]+" "+aria_label[-8]
        uploaded_video_details["views"].append(views)
        uploaded_video_details["date_of_upload"].append(uploaded_period)
        uploaded_video_details["video_length"].append(video_length)
    df=pd.DataFrame.from_dict(uploaded_video_details)
    return df
# Scrolling Youtube video page to complete bottom to scrape all video
def scroll_page_down(driver):
    WAIT_IN_SECONDS = 2
    #scrolling the  webpage to bottom 
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll to the bottom of page
        driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        # Wait for new videos to show up
        time.sleep(WAIT_IN_SECONDS)
        
        # Calculate new document height and compare it with last height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver
# Scrapping Any YouTube Channel page
def youtube_videos_dataframe(search):
    driver=get_driver()
    driver.get(f"https://www.youtube.com/@{search}/videos")
    driver=scroll_page_down(driver)
    df= scrape_videos(driver)
    return df









