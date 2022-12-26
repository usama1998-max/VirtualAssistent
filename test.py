# FOR TESTING PURPOSE ONLY !

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from win32com.client import Dispatch
import pyttsx3


search_bar = "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input"

search_btn = "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/button"

first_video = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a"

video_settings = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[30]"


play_bar = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div"

p720 = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[27]/div/div[2]/div[2]"
p360 = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[27]/div/div[2]/div[4]"
p_auto = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[27]/div/div[2]/div[7]"

nxt_vid = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[29]/div[2]/div[1]/a[2]"


def speech_text():
    import speech_recognition as sr

    r = sr.Recognizer()
    m = sr.Microphone()
    string = ""

    with m as source:
        r.adjust_for_ambient_noise(source, duration=3)

        print("Listening...")
        audio = r.listen(source)
        time.sleep(1)

        try:
            string = r.recognize_google(audio, language="ur-PK")
            print("You said: ", string)
        except Exception as e:
            print(e)

    return string


pause_btn = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[28]/div[2]/div[1]/button"
skip_ad = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[4]/div/div[3]/div/div[2]/span/button"

contents = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]"
link = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer[1]/div[1]/div[2]/ytd-vertical-list-renderer/div[1]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string"

settings = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[31]/div[2]/div[2]/button[3]"

quality = """/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[29]/div/div/div[3]/div[2]"""

p720 = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[27]/div/div[2]/div[2]"
p360 = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[27]/div/div[2]/div[4]"
p_auto = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[27]/div/div[2]/div[7]"

play_btn = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div"


def pause(web_driver):
    try:
        pbtn = web_driver.find_element(By.XPATH, pause_btn)
        web_driver.implicitly_wait(5)
        print(pbtn.is_displayed())
        pbtn.click()
    except NoSuchElementException as e:
        print(e)


def search_video(web_driver, string=""):
    search = web_driver.find_element(By.XPATH, search_bar)
    web_driver.implicitly_wait(2)
    search.clear()
    web_driver.implicitly_wait(2)

    if string != "":
        search.send_keys(string)
        web_driver.implicitly_wait(2)
        search.send_keys(Keys.RETURN)
    else:
        print("You did not provide parameter 'string' !")

    web_driver.implicitly_wait(5)


def skip_ads(web_driver):
    try:
        ads = web_driver.find_element(By.XPATH, skip_ad)
        web_driver.implicitly_wait(20)

        while ads.is_displayed() is False:
            print("No ads yet!")
            time.sleep(2)

        if ads.is_displayed() is True:
            print("Ad skipped!")
            ads.click()
    except NoSuchElementException as e:
        print("No ads")


def play(web_driver):
    btn = web_driver.find_element(By.XPATH, play_bar)
    web_driver.implicitly_wait(2)
    btn.send_keys(Keys.SPACE)


def click_first_video(web_driver):
    video = web_driver.find_element(By.XPATH, first_video)
    web_driver.implicitly_wait(10)
    video.click()

    web_driver.implicitly_wait(10)


def search_video(web_driver, string: str):
    SEARCH_URL = f"https://www.youtube.com/results?search_query="

    SEARCH_URL += string

    web_driver.implicitly_wait(5)
    web_driver.get(SEARCH_URL)


if __name__ == "__main__":
    # URL = "https://www.youtube.com/watch?v=ntO9nRr_sbw"
    # URL2 = "https://www.youtube.com/"
    #
    # driver = webdriver.Chrome()
    # driver.get(URL)
    # driver.implicitly_wait(15)
    #
    # skip_ads(driver)
    #
    # time.sleep(3)
    #
    # video_settings = driver.find_element(By.CSS_SELECTOR, "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-right-controls > button.ytp-size-button.ytp-button")
    # video_settings.click()
    # driver.implicitly_wait(5)

    cmd = speech_text()
    print(cmd)
