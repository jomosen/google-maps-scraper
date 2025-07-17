import os
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

WAIT_TIMEOUT = 10
SCROLL_PAUSE_TIME = 1

class SeleniumDriver():
    def __init__(self, options = Options()):
        self.driver = self.get_stealth_driver(options)

    def get_stealth_driver(self, options):
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "./chromedriver.exe")

        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(
                f"ChromeDriver not found in {chromedriver_path}. "
                "Please set the CHROMEDRIVER_PATH environment variable "
                "or place chromedriver.exe in the root of the project."
            )
    
        
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            });
            """
        })

        return driver
    
    def load_url(self, url):
        self.driver.get(url)
    
    def get_elements(self, selector_value):
        return self.driver.find_elements(By.CSS_SELECTOR, selector_value)
    
    def get_element(self, selector_value):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, selector_value)
        except NoSuchElementException:
            return None
    
    def get_element_attribute(self, selector_value, attribute):
        element = self.get_element(By.CSS_SELECTOR, selector_value, attribute)
        if element:
            return element.get_attribute(attribute)
        return None
    
    def get_element_text(self, selector_value):
        element = self.get_element(By.CSS_SELECTOR, selector_value)
        if element:
            return element.text
        return None
    
    def get_elements_within_parent(self, parent, element_selector_value):
        return parent.find_elements(By.CSS_SELECTOR, element_selector_value)
    
    def get_element_within_parent(self, parent, element_selector_value):
        try:
            return parent.find_element(By.CSS_SELECTOR, element_selector_value)
        except NoSuchElementException:
            return None
    
    def get_element_attribute_within_parent(self, parent, element_selector_value, attribute):
        element = self.get_element_within_parent(parent, element_selector_value)
        if element:
            return element.get_attribute(attribute)
        return None
    
    def get_element_text_within_parent(self, parent, element_selector_value):
        element = self.get_element_within_parent(parent, element_selector_value)
        if element:
            return element.text
        return None

    def click_element_when_present(self, selector_value):
        try:
            element = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector_value))
            )
            element.click()
        except NoSuchElementException:
            print(f"Element with selector '{selector_value}' not found.")
        except Exception as e:
            print(f"Unexpected error while clicking element: {e}")

    def send_keys_after_waiting(self, selector_value, input_value):
        try:
            input_element = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector_value))
            )

            input_element.send_keys(Keys.CONTROL, 'a')
            time.sleep(random.uniform(0.1, 0.2))
            input_element.send_keys(Keys.DELETE)
            time.sleep(random.uniform(0.1, 0.2))

            for char in input_value:
                input_element.send_keys(char)
                time.sleep(random.uniform(0.025, 0.125))

            time.sleep(random.uniform(0.2, 0.4))
            input_element.send_keys(Keys.ENTER)

        except NoSuchElementException:
            print(f"Input field with selector '{selector_value}' not found.")
        except Exception as e:
            print(f"Unexpected error while sending keys: {e}")

    def scroll_element(self, selector_value, number_of_times=100, selector_type=By.CSS_SELECTOR):
        element = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((selector_type, selector_value))
        )

        previous_scroll_height = self.driver.execute_script("return arguments[0].scrollHeight", element)
        end_reached = False
        i = 0
        while not end_reached and i < number_of_times:
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)

            time.sleep(SCROLL_PAUSE_TIME)

            new_scroll_height = self.driver.execute_script("return arguments[0].scrollHeight", element)
            if new_scroll_height == previous_scroll_height:
                end_reached = True

            previous_scroll_height = new_scroll_height
            i += 1

    def scroll_element_by_xpath(self, xpath_value, number_of_times=100):
        return self.scroll_element(xpath_value, number_of_times, By.XPATH)

    def get_parents_of_elements(self, selector_value):
        return [el.find_element(By.XPATH, "..") for el in self.driver.find_elements(By.CSS_SELECTOR, selector_value)]
    
    def scroll_until_element_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)