# Bot Code

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from small_functions import get_name_age


def setup_headless():
    """
    function to initialize the headless chromium and ChromeDriver
    :return:
    """
    # Setting Options for headless Chromium
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    # Block Ads
    prefs = {
        "profile.managed_default_content_settings.ads": 2,  # Disable Ads
        "profile.default_content_setting_values.popups": 2,  # Disable Pop-ups 
        "profile.managed_default_content_settings.images": 2,  # Disable images to speed up loading
    }

    options.add_experimental_option("prefs", prefs)

    # Set up the WebDriver (Ensure you have the appropriate ChromeDriver installed)

    # driver = webdriver.Chrome(service=Service("./drivers/chromedriver/chromedriver"),
    #                           options=options)  # uncomment if driver not found in termux or linux

    driver = webdriver.Chrome(options=options)  # Comment this if above line in uncomment

    return driver


def create_tabs(driver):
    """
    function for creating the temp-mail and target site browser tabs
    :parameter: driver
    :return: string -> Tabs Created
    """
    # Open Temp mail
    driver.get('https://www.guerrillamail.com/')

    # Open a new window and switch to it
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    # Open Hipi in the new window
    driver.get('https://www.hipi.co.in/')

    # Switch back to the first window (Temp-Mail)
    driver.switch_to.window(driver.window_handles[0])

    return "Tabs Created"


# def get_temp_mail(driver):
#     """
#     This function copies the temporary mail form the temp-mail website and return it
#     :parameter: driver
#     :return: temp_mail_
#     """
#     driver.refresh()

#     check_box = driver.find_element("id", "use-alias")
#     check_box.click()

#     mail_field = driver.find_element("id", "email-widget")
#     temp_mail_ = str(mail_field.text)
#     print(f"Mail : {temp_mail_}")

#     return temp_mail_


def get_temp_mail(driver):
    """
    This function copies the temporary mail form the temp-mail website and return it
    :parameter: driver
    :return: temp_mail_
    """

    user_name, user_age, user_gender = get_name_age(func_name="get_temp_mail")
    user_initials = user_name.replace(" ", f'{user_age}').lower()

    driver.refresh()

    initial_btn = driver.find_element(By.ID, "inbox-id")
    unique_string = initial_btn.text[:4]
    initial_btn.click()

    new_initials = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/span[1]/span/input")
    new_initials.send_keys(f"{user_initials}{unique_string}")
    new_initials.send_keys(Keys.RETURN)

    check_box = driver.find_element(By.ID, "use-alias")
    check_box.click()

    mail_field = driver.find_element(By.ID, "email-widget")
    temp_mail = mail_field.text
    print(f"Mail : {temp_mail}")

    return temp_mail


def sign_up(driver, temp_mail):
    """
    function for creating account in Hipi And requesting otp from temp-mail
    :parameter: driver
    :return: user_name, user_age, user_gender and usr_data
    """

    sign_up_btn = driver.find_element("xpath", "/html/body/div/div[1]/div/div[1]/div/div[3]/button")
    sign_up_btn.click()
    time.sleep(1)

    use_mail = driver.find_element("xpath", "/html/body/div/div[3]/div/div/div[2]/div[1]/div/div[2]")
    use_mail.click()

    mail_input_box = driver.find_element("xpath", "/html/body/div/div[3]/div/div[2]/div/div/form/input")
    mail_input_box.send_keys(str(temp_mail))
    # time.sleep(2)

    proceed_btn = driver.find_element("xpath", "/html/body/div/div[3]/div/div[2]/div/div/form/div/button")
    proceed_btn.click()
    # time.sleep(2)

    user_name, user_age, user_gender = get_name_age(func_name="sign_up")

    usr_data = True

    print("sign_up() done.")

    return user_name, user_age, user_gender, usr_data


def request_otp(driver, usr_name, usr_gender, usr_age):
    """
    function for requesting otp form temp-mail for account [ successor of the sign_up() function ]
    :return: sting -> OTP Requested
    """
    
    # Wait for the username field to be present and then send the username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    username_field.send_keys(str(usr_name))
    
    # time.sleep(2)
    
    # username_field = driver.find_element("id", "name")
    # username_field.send_keys(str(usr_name))

    if usr_gender == "Male":
        gender_m = driver.find_element("xpath", "/html/body/div/div[3]/div/div[2]/form/div[3]/select/option[2]")
        gender_m.click()
    else:
        gender_f = driver.find_element("xpath", "/html/body/div/div[3]/div/div[2]/form/div[3]/select/option[3]")
        gender_f.click()

    age_field = driver.find_element("id", "dob")
    age_field.send_keys(str(usr_age))
    # time.sleep(2)

    submit_btn = driver.find_element("xpath", "/html/body/div/div[3]/div/div[2]/form/div[5]/button")
    submit_btn.click()

    print("request_otp() done")

    return "OTP Requested"


def copy_otp(driver):
    """
    Function for copying OTP from temp-mail
    :return: hipi_otp_ -> The OTP requested by hipi to Temp-mail
    """
    start_time = time.time()
    # try:
    #     consent_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]")
    # except:
    #     consent_btn = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]")
    #
    # consent_btn.click()

    print("Waiting for the otp...")

    # Initialize the WebDriverWait with a timeout
    wait = WebDriverWait(driver, 3)  # 4 seconds max waiting time

    # this the xpath of second row in the mail table which will only come when the
    # opt message come to temp-mail
    _xpath_to_found = "/html/body/div[4]/div/div[3]/div[2]/form/table/tbody/tr[2]"
    element_found = False

    # while loop to check if otp found or not
    while not element_found:
        try:
            # Try to find the element using the provided XPath
            element = wait.until(EC.presence_of_element_located((By.XPATH, _xpath_to_found)))
            element_found = True
            print("Element found at the specified XPath.")
        except:
            # print("Element not found, refreshing again...")
            driver.refresh()
            # time.sleep(2)
            continue

    time.sleep(1)

    try:
        hipi_mail_box = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[3]/div[2]/form/table/tbody/tr[1]/td[3]/a")
    except:
        hipi_mail_box = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[3]/div[2]/form/table/tbody/tr/td[3]")

    hipi_otp_ = str(hipi_mail_box.text).lstrip()[:4]
    print("The OTP is : ", hipi_otp_)

    end_time = time.time()
    seconds = int(end_time) - int(start_time)

    minutes, remaining_seconds = divmod(seconds, 60)

    print("copy_otp() done")
    print(f"time to copy OTP : {minutes}:{remaining_seconds}")

    return hipi_otp_


def verify_otp(driver, hipi_otp):
    """
    function for submitting otp back to the hipi and verify it and completing sign up
    :return: string -> OTP Verification Successful - User Logged In
    """

    send_otp = driver.find_element("xpath", "/html/body/div/div[3]/div/div[2]/form/div[5]/div[1]/input")
    send_otp.send_keys(hipi_otp)

    verify_otp_btn = driver.find_element("xpath", "/html/body/div/div[3]/div/div[2]/form/div[5]/div[2]/button")
    verify_otp_btn.click()
    time.sleep(2)
    driver.refresh()
    time.sleep(2)
    driver.refresh()

    print("verify_otp() done.")

    return "OTP Verification Successful - User Logged In"


# def following(driver, creator_name):
    # """
    # function responsible for increasing the followers of specified channels
    # :parameter: driver, creator_name -> takes the name of channel as the parameter
    # :return: follow_num -> Followers Count of the channel name
    # """

    # # Creating New Tab for Creator Channel
    # # Open a new window and switch to it
    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[2])

    # # Open the new window with the creator name searched in it
    # driver.get(f'https://www.hipi.co.in/@{creator_name}')

    # time.sleep(2)

    # follow_click = driver.find_element("xpath", "/html/body/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]/button")

    # follow_click.click()

    # print("Follow Button Click")

    # # Initialize the WebDriverWait with a timeout
    # wait = WebDriverWait(driver, 2)  # 2 seconds

    # # Follow button xpath
    # follow_btn = "/html/body/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]/button"
    # element_found = False

    # while not element_found:

        # driver.refresh()

        # try:
            # # Try to find the element using the provided XPath
            # element = wait.until(EC.presence_of_element_located((By.XPATH, follow_btn)))
            # # element = wait.until(EC.visibility_of_element_located((By.XPATH, follow_btn)))
            # if str(element.text) == "Following":
                # element_found = True  # Element is found, break the loop
                # print(f"{creator_name} : Followed")
        # except:
            # # If the element is not found, continue refreshing
            # print(f"{creator_name} : Not Followed")
            # print("refreshing again...")
            # continue

    # driver.refresh()
    # time.sleep(1)
    # driver.refresh()

    # follow_count = driver.find_element("xpath", "/html/body/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/p[1]")
    # # follow_count = driver.find_element("xpath", "/html/body/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]")
    # follow_num = str(follow_count.text)
    # print(f"{creator_name} Followers Count : {follow_num}")

    # return follow_num


# # "https://www.hipi.co.in/search?term=123laughtergo" ✔
# # "https://www.hipi.co.in/@123laughtergo"


# # "https://www.hipi.co.in/search?term=everydaylifestyle"
# # "https://www.hipi.co.in/@everydaylifestyle"


def following(driver, creator_name, max_retries=2):
    """
    Function responsible for increasing the followers of specified channels
    :parameter: driver, creator_name -> takes the name of channel as the parameter
    :return: follow_num -> Followers Count of the channel name
    """
    for attempt in range(max_retries):
        try:
            # Creating New Tab for Creator Channel
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[2])

            # Open the new window with the creator name searched in it
            driver.get(f'https://www.hipi.co.in/@{creator_name}')
            time.sleep(2)

            # Try clicking the follow button
            follow_click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]/button"))
            )
            follow_click.click()
            print("Follow Button Clicked")

            # Wait until the button text changes to "Following"
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]/button").text == "Following"
            )
            print(f"{creator_name} : Followed")

            # Refresh to get the updated follower count
            driver.refresh()
            time.sleep(1)
            driver.refresh()

            follow_count = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/p[1]")
            follow_num = str(follow_count.text)
            print(f"{creator_name} Followers Count : {follow_num}")

            return follow_num
        
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying...")
                driver.refresh()  # Refresh the page and try again
                time.sleep(2)  # Wait a bit before retrying
            else:
                print("Max retries reached. Exiting.")
                return None

# Example usage
# follow_num = following(driver, 'everydaylifestyle')

# Error : Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="name"]"}
  # (Session info: chrome=125.0.6422.141)