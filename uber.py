import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchElementException
import random
from time import sleep
 
class Uber:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    @staticmethod
    def human_like_typing(element, text, min_delay=0, max_delay=0.2):
        for character in text:
            delay = random.uniform(min_delay, max_delay)
            element.send_keys(character)
            time.sleep(delay)

    @staticmethod
    def request():
        pass
    
    @staticmethod
    def wait_for_otp_code(inbox_manager, email):
     otp_code = None
     attempts = 0
     while not otp_code and attempts < 10:  
        time.sleep(5) 
        print("Checking for OTP code...")
        messages = inbox_manager.get_all_messages(email)
        if messages:
            last_message_uid = messages[-1]['uid']  # Assuming messages is a list of dicts with 'uid'
            message_content = inbox_manager.get_message_content(last_message_uid)
            html_content = message_content.get('html', '')
            otp_code = inbox_manager.get_code(html_content)  # Assuming get_code returns the code as a string
            if otp_code:
                print(f"OTP code found: {otp_code}")
                break
        attempts += 1
     return otp_code

    @staticmethod
    def signup(first_name, last_name, email, password, inbox_manager):
        options = uc.ChromeOptions()
        # You can add additional options as needed, for example:
        # options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        try:
            driver.get('https://ubereats.com/')
            sleep(2)
            login_xpan = '//*[@id="wrapper"]/header/div/div/div/div/a[2]'
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, login_xpan))).click()
            sleep(3)
             # Step 0
            email_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'PHONE_NUMBER_or_EMAIL_ADDRESS')))
            Uber.human_like_typing(email_field, email)
            time.sleep(random.uniform(1, 2))  # Random sleep to mimic human delay
            driver.find_element(By.ID, 'forward-button').click()

            otp_code = Uber.wait_for_otp_code(inbox_manager, email)
            if otp_code:
                # Step 1: Enter OTP
                for i, digit in enumerate(otp_code):
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f'EMAIL_OTP_CODE-{i}'))).send_keys(digit)
                driver.find_element(By.ID, 'forward-button').click()

            driver.find_element(By.ID, 'forward-button').click()

            # Step 2
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'alt-SKIP'))).click()

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'FIRST_NAME'))).send_keys(first_name)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'LAST_NAME'))).send_keys(last_name)
            driver.find_element(By.ID, 'forward-button').click()
            sleep(2)
            checkbox_xpath = "//*[@id='LEGAL_ACCEPT_TERMS']/span"
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath))).click()
            sleep(2)
            driver.find_element(By.ID, 'forward-button').click()
            sleep(2)
            driver.get('https://www.ubereats.com/de/invite')
            sleep(2)

        except (TimeoutException, UnexpectedAlertPresentException, NoSuchElementException) as e:
            print(f"An error occurred: {e}")
            pass
        finally:
            driver.close()
            time.sleep(5)

        return Uber(email, password)