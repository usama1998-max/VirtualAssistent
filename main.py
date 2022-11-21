from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pyttsx3
import time

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
            print("اشتہار ترک کرنے کا اختیار نہیں!")
            time.sleep(3)

        engine.say("skipping boring ad")
        engine.runAndWait()

        if ads.is_displayed() is True:
            print("اشتہار ترک کر دیا!")
            ads.click()
    except NoSuchElementException:
        print("اشتہار نہیں ملے!")


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
            print("سن رہا ہوں...")

        if speak is True:
            engine.say(message)
            engine.runAndWait()

        print("بولو...")
        audio = r.listen(source)

        try:
            string = r.recognize_google(audio, language="ur-PK")
            print("آپ نے کہا: ", string)
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

    if option == "زیادہ کرو" or option == "زیادہ" or option == "زیادہ کر دو":
        for i in range(len(pixel)):
            if pixel[i].text == "720p":
                pixel[i].click()
                break
        engine.say("quality set to high")
        engine.runAndWait()

    if option == "کم کرو" or option == "کم" or option == "کم کر دو":
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


# Main Function
def main() -> None:
    driver = None

    print("---- Virtual Assistant ----")
    engine.say("welcome to virtual assistant")
    engine.runAndWait()

    URL = "https://www.youtube.com/"
    URL_QUERY = "https://www.youtube.com/results?search_query="

    while True:

        call_ai = speech(False, print_dialogue=False)

        if call_ai == "بات سنو":
            command = speech(True, "Listening")

            if command == "انٹرنیٹ کھولو" or command == "نیٹ کھولو":
                engine.say("openning browser")
                engine.runAndWait()
                driver = webdriver.Chrome()

            if command == "یوٹیوب" or command == "یوٹیوب کھولیں" or command == "یوٹیوب کھولو":
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
                        URL_QUERY += search_video

                        driver.implicitly_wait(5)
                        driver.get(URL_QUERY)

            if command == "ویڈیو ڈھونڈو":
                search_video(driver)

            if command == "چلاؤ" or command == "شروع کرو":
                if driver is None:
                    print("یوٹیوب کھولو پہلے!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    pause(driver)

            if command == "پہلی ویڈیو":
                if driver is None:
                    print("یوٹیوب کھولو پہلے!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    engine.say("playing first video")
                    engine.runAndWait()
                    click_first_video(driver)

            if command == "رک جاؤ":
                if driver is None:
                    print("یوٹیوب کھولو پہلے!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    pause(driver)

            if command == "اشتہار ہٹاؤ":
                if driver is None:
                    print("یوٹیوب کھولو پہلے!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    skip_ads(driver)

            if command == "اوپر کرو" or command == "اوپر جاؤ" or command == "اوپر آؤ":
                if driver is None:
                    print("یوٹیوب کھولو پہلے!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    driver.execute_script("window.scrollBy(0, -500)")
                    driver.implicitly_wait(1)

            if command == "نیچے آؤ" or command == "نیچے کرو" or command == "نیچے جاؤ":
                driver.execute_script("window.scrollBy(0, 500)")
                driver.implicitly_wait(1)

            if command == "کوالٹی کھولو" or command == "ویڈیو کوالٹی":
                if driver is None:
                    print("یوٹیوب کھولو پہلے!")
                    engine.say("Maybe open youtube first")
                    engine.runAndWait()
                else:
                    set_quality(driver)
                    driver.implicitly_wait(2)

            if command == "بند کرو":
                break


if __name__ == "__main__":
    main()
