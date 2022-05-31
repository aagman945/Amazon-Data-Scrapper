import pytesseract
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import cv2

def resolve_captcha(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    img=cv2.imread(path)
    return pytesseract.image_to_string(img)

def get_captcha():
    url = f"https://www.amazon.com/errors/validateCaptcha"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(3)
    captcha = driver.find_element(by = By.CSS_SELECTOR,value = 'img') 
    captcha_url = captcha.get_attribute("src")
    print(captcha_url)
    time.sleep(3)
    urllib.request.urlretrieve(captcha_url,'screenshot.png')
    value = resolve_captcha('screenshot.png')
    print(value)
    text_area = captcha = driver.find_element(By.ID,'captchacharacters')
    time.sleep(5)
    text_area.send_keys(value)
    time.sleep(2)
    text_area.send_keys(Keys.ENTER)

if __name__ == "__main__":
    get_captcha()


