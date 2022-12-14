import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pyttsx3
import time
from interface import main


# Text to Speech
engine = pyttsx3.init("sapi5")

# Setting speaking rate
engine.setProperty("rate", 170)

# XPATH to first video link
first_video = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[" \
              "1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[" \
              "2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a "

# XPATH to skip add button
skip_ad = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[" \
          "2]/div/div/ytd-player/div/div/div[17]/div/div[3]/div/div[2]/span/button "

# XPATH to pause/play button
pause_btn = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[" \
            "2]/div/div/ytd-player/div/div/div[28]/div[2]/div[1]/button "


# SELECTOR PATH to next video button
nxt_vid = "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls" \
          " > div.ytp-left-controls > a.ytp-next-button.ytp-button"


# cinema mode selector
cinema_screen = "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls >" \
                " div.ytp-right-controls > button.ytp-size-button.ytp-button"


# full screen mode selector
full_screen = "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls >" \
              " div.ytp-right-controls > button.ytp-fullscreen-button.ytp-button"


# volume button selector
volume_button = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]" \
                "/div/div/ytd-player/div/div/div[32]/div[2]/div[1]/span/button"


# Function for clicking on first video on page
def click_first_video(web_driver: webdriver):
    video = web_driver.find_element(By.XPATH, first_video)
    web_driver.implicitly_wait(10)
    video.click()

    web_driver.implicitly_wait(10)


# Function for skipping ADs
def skip_ads(web_driver: webdriver) -> None:
    try:
        ads = web_driver.find_element(By.XPATH, skip_ad)
        web_driver.implicitly_wait(20)

        while ads.is_displayed() is False:
            print("???????????? ?????? ???????? ???? ???????????? ????????!")
            time.sleep(3)

        engine.say("skipping boring ad")
        engine.runAndWait()

        if ads.is_displayed() is True:
            print("???????????? ?????? ???? ??????!")
            ads.click()
    except NoSuchElementException:
        print("???????????? ???????? ??????!")


# Function for speech detection in URDU
def speech(speak: bool, message: str = "", print_dialogue: bool = True) -> str:
    # SpeechRecognition should be imported inside a function
    # to create multiple sessions
    import speech_recognition as sr

    r = sr.Recognizer()
    m = sr.Microphone()
    string = ""

    with m as source:
        r.adjust_for_ambient_noise(source, duration=1)

        if print_dialogue is True:
            print("???? ?????? ??????...")

        if speak is True:
            engine.say(message)
            engine.runAndWait()

        print("????????...")
        audio = r.listen(source)

        try:
            string = r.recognize_google(audio, language="ur-PK")
            print("???? ???? ??????: ", string)
        except Exception as e:
            print(e)

    return string


# Function for playing or pausing video
def pause(web_driver: webdriver) -> None:
    try:
        pbtn = web_driver.find_elements(By.CLASS_NAME, "ytp-play-button")
        web_driver.implicitly_wait(5)
        pbtn[0].click()
    except NoSuchElementException as e:
        print(e)


# Function for setting video quality
def set_quality(web_driver: webdriver) -> None:
    video_settings = web_driver.find_element(By.CLASS_NAME, "ytp-settings-button")
    web_driver.implicitly_wait(5)
    video_settings.click()

    web_driver.implicitly_wait(5)

    time.sleep(7)

    quality_btn = web_driver.find_elements(By.CLASS_NAME, "ytp-menuitem-label")
    web_driver.implicitly_wait(2)

    for i in range(len(quality_btn)):
        if quality_btn[i].text == "Quality":
            quality_btn[i].click()

    time.sleep(5)

    pixel = web_driver.find_elements(By.CLASS_NAME, "ytp-menuitem-label")
    web_driver.implicitly_wait(2)

    option = speech(True, "speak to set quality", False)

    if option == "?????????? ??????" or option == "??????????" or option == "?????????? ???? ????":
        for i in range(len(pixel)):
            if pixel[i].text == "720p":
                pixel[i].click()
                break
        engine.say("quality set to high")
        engine.runAndWait()

    if option == "???? ??????" or option == "????" or option == "???? ???? ????":
        for i in range(len(pixel)):
            if pixel[i].text == "360p":
                pixel[i].click()
                break
        engine.say("quality set to low")
        engine.runAndWait()


# Function for searching video
def search_video(web_driver: webdriver) -> None:

    query = speech(True, "speak to search", True)

    SEARCH_URL = f"https://www.youtube.com/results?search_query="

    SEARCH_URL += query

    web_driver.implicitly_wait(5)
    web_driver.get(SEARCH_URL)


# Function for playing next video
def next_video(web_driver: webdriver) -> None:
    try:
        nv = web_driver.find_element(By.CSS_SELECTOR, nxt_vid)
        nv.click()
        web_driver.implicitly_wait(2)
    except NoSuchElementException:
        print("Try again")


def cinema_screen_mod(web_driver: webdriver) -> None:
    cm = web_driver.find_element(By.CSS_SELECTOR, cinema_screen)
    cm.click()
    web_driver.implicitly_wait(2)


def screen_mod(web_driver: webdriver) -> None:
    cm = web_driver.find_element(By.CSS_SELECTOR, full_screen)
    cm.click()
    web_driver.implicitly_wait(2)


def volume_mod(web_driver: webdriver) -> None:
    vm = web_driver.find_element(By.XPATH, volume_button)
    vm.click()
    web_driver.implicitly_wait(2)


# Main Function
def virtual_assistant() -> None:
    driver = None

    print("---- Virtual Assistant ----")
    engine.say("welcome to virtual assistant")
    engine.runAndWait()

    URL = "https://www.youtube.com/"
    URL_QUERY = "https://www.youtube.com/results?search_query="

    while True:

        call_ai = speech(False, print_dialogue=False)

        if call_ai == "?????? ??????":

            command = speech(True, "Listening")

            if command == "?????????????? ??????????" or command == "?????? ??????????":
                engine.say("openning browser")
                engine.runAndWait()
                driver = webdriver.Chrome()

            if command == "????????????" or command == "???????????? ????????????" or command == "???????????? ??????????":
                if driver is None:
                    engine.say("getting youtube")
                    engine.runAndWait()

                    driver = webdriver.Chrome()
                    driver.get(URL)

                else:
                    engine.say("getting youtube")
                    engine.runAndWait()
                    driver.get(URL)
                    driver.implicitly_wait(5)

                    search_query = speech(True, "Speak to search video")

                    if search_query == "":
                        engine.say("You didn't speak anything")
                        engine.runAndWait()
                    else:
                        URL_QUERY += search_query

                        driver.implicitly_wait(5)
                        driver.get(URL_QUERY)

            if command == "?????????? ????????????":
                search_video(driver)

            if command == "????????" or command == "???????? ??????":
                if driver is None:
                    print("???????????? ?????????? ????????!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    pause(driver)

            if command == "???????? ??????????":
                if driver is None:
                    print("???????????? ?????????? ????????!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    engine.say("playing first video")
                    engine.runAndWait()
                    click_first_video(driver)

            if command == "???? ??????":
                if driver is None:
                    print("???????????? ?????????? ????????!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    pause(driver)

            if command == "???????????? ????????":
                if driver is None:
                    print("???????????? ?????????? ????????!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    skip_ads(driver)

            if command == "???????? ??????" or command == "???????? ??????" or command == "???????? ????":
                if driver is None:
                    print("???????????? ?????????? ????????!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    driver.execute_script("window.scrollBy(0, -500)")
                    driver.implicitly_wait(1)

            if command == "???????? ????" or command == "???????? ??????" or command == "???????? ??????":
                driver.execute_script("window.scrollBy(0, 500)")
                driver.implicitly_wait(1)

            if command == "???????????? ??????????" or command == "?????????? ????????????":
                if driver is None:
                    print("???????????? ?????????? ????????!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    set_quality(driver)
                    driver.implicitly_wait(2)

            if command == "???????? ?????????? ????????" or command == "???????? ??????????":
                next_video(driver)

            if command == "?????????? ??????":
                driver.back()

            if command == "?????? ????????":
                driver.forward()

            if command == "??????????":
                cinema_screen_mod(driver)

            if command == "???? ??????????" or command == "?????????? ?????? ??????" or command == "?????? ??????????":
                screen_mod(driver)

            if command == "?????????? ??????????" or command == "?????????? ???????????? ??????" or command == "?????????? ?????????? ??????":
                screen_mod(driver)

            if command == "???????? ?????? ??????":
                volume_mod(driver)

            if command == "???????? ??????????":
                volume_mod(driver)

            if command == "?????? ??????":
                exit(0)
                break


t1 = threading.Thread(target=main)

t1.start()
virtual_assistant()
