import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract

# Specify the path to Tesseract explicitly
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Sample data
emails = [
    "StephaneAndor202@outlook.com",
]
phone_numbers = [
    "61-925-564-554",
]
default_password = "123!@#qweQWE"
isd_code = "+61 - Australia"

# Generate random username and full name
def generate_random_username():
    return "User" + str(random.randint(100, 999))

def generate_random_fullname():
    first_names = ["John", "Jane", "Alex", "Emily"]
    last_names = ["Smith", "Johnson", "Brown", "Taylor"]
    return random.choice(first_names) + " " + random.choice(last_names)

def click_ok_button(driver):
    try:
        # Wait for the "OK" button to appear and click it
        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "col-xs-offset-3"))
        )
        ok_button.click()
        print("OK button clicked successfully!")
    except Exception as e:
        print(f"Error clicking OK button: {e}")

def wait_for_and_click_verify_button(driver):
    try:
        # Wait for the OTP input field to appear
        otp_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "enterOTPEmail"))
        )

        # Prompt user to enter OTP manually in the terminal
        otp_code = input("Verify Code: ")  # User types OTP in the terminal

        # Enter the OTP in the browser
        otp_input.send_keys(otp_code)

        # Simulate pressing "Enter" after typing the OTP
        otp_input.send_keys("\n")

        # Click the "Verify Email Id with OTP" button
        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn btn-primary"))
        )
        verify_button.click()
        print("Verification code submitted successfully!")
    except Exception as e:
        print(f"Error during verification code submission: {e}")

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open signup page
    driver.get("https://www.irctc.co.in/nget/profile/user-signup")
    time.sleep(3)  # Wait for page to load

    # Fill username
    username = generate_random_username()
    driver.find_element(By.ID, "userName").send_keys(username)
    print(f"Username: {username}")

    # Fill full name
    full_name = generate_random_fullname()
    driver.find_element(By.ID, "fullName").send_keys(full_name)
    print(f"Full Name: {full_name}")

    # Fill password
    driver.find_element(By.ID, "usrPwd").send_keys(default_password)
    print("Password: Filled")

    # Confirm password
    driver.find_element(By.ID, "cnfUsrPwd").send_keys(default_password)
    print("Confirm Password: Filled")

    # Fill email
    email = random.choice(emails)
    driver.find_element(By.ID, "email").send_keys(email)
    print(f"Email: {email}")

    # Select ISD code
    try:
        isd_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[type='text']"))
        )
        isd_dropdown.click()
        time.sleep(1)  # Allow dropdown to appear

        # Select Australia option
        australia_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[@value='+61 - Australia']"))
        )
        australia_option.click()
        print(f"ISD Code: {isd_code}")
    except Exception as e:
        print(f"Error selecting ISD code: {e}")

    # Fill phone number
    phone_number = random.choice(phone_numbers)
    driver.find_element(By.ID, "mobile").send_keys(phone_number)
    print(f"Phone Number: {phone_number}")

    # Solve CAPTCHA
    try:
        captcha_image = driver.find_element(By.CLASS_NAME, "captcha-img")
        captcha_src = captcha_image.screenshot_as_png  # Capture CAPTCHA as an image

        # Save and read the CAPTCHA image
        captcha_file = "captcha.png"  # Specify the file name
        with open(captcha_file, "wb") as file:
            file.write(captcha_src)
        captcha_text = pytesseract.image_to_string(Image.open(captcha_file)).strip()

        # Enter CAPTCHA text
        driver.find_element(By.ID, "captcha").send_keys(captcha_text)
        print(f"CAPTCHA: {captcha_text}")
    except Exception as e:
        print(f"Error solving CAPTCHA: {e}")

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    print("Form submitted successfully!")

    # Click the OK button after submission
    click_ok_button(driver)

    # Wait for the user to type the OTP in the terminal and click verify
    wait_for_and_click_verify_button(driver)

    time.sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()



