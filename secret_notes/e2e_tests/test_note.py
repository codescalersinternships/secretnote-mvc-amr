import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By


def test_create_view_note():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("http://localhost:8000/note/create/")

        time.sleep(1)

        textarea = driver.find_element(By.NAME, "content")
        textarea.send_keys("New note")

        expiration_time = driver.find_element(By.NAME, "expiration")
        expiration_time.send_keys('1')

        submit_button = driver.find_element(By.XPATH, '//button[contains(text(), "Create Note")]')
        submit_button.click()

        time.sleep(1)

        assert "Note created!" in driver.page_source

        link = driver.find_element(By.XPATH, "//a")
        link.click()

        time.sleep(1)

        assert "New note" in driver.page_source

        driver.refresh()
        time.sleep(1)

        assert "This note has expired or reached its view limit." in driver.page_source

    finally:
        driver.quit()