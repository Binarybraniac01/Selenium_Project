# Main Code

import time
import argparse
from bot.bot_v2 import *
from small_functions import user_data_counter


# Create the Parser
parser = argparse.ArgumentParser(description="This script accepts command-line arguments.")

# Add Arguments
parser.add_argument('--limit', type=int, required=True, help="Loop limit value.\nUsage : python3 main.py --limit 5")
# parser.add_argument('--client', type=int, default=1, help="Loop limit value.\nUsage : python3 main.py --limit 5")

# Parse the arguments
args = parser.parse_args()


# Setting loop for Repetitive Following
counter = 0
while counter <= args.limit:
    start_time = time.time() # Capture the start time
    usr_data = False
    
    try:
        _driver = setup_headless()

        create_tabs(driver=_driver)

        temp_mail = get_temp_mail(driver=_driver)

        _driver.switch_to.window(_driver.window_handles[1])

        usr_name, usr_age, usr_gender, usr_data = sign_up(driver=_driver, temp_mail=temp_mail)

        print(f"Name : {usr_name}, Age: {usr_age}, Gender: {usr_gender}")

        request_otp(driver=_driver, usr_name=usr_name, usr_age=usr_age, usr_gender=usr_gender)

        _driver.switch_to.window(_driver.window_handles[0])

        time.sleep(2)

        _hipi_otp = copy_otp(driver=_driver)

        _driver.switch_to.window(_driver.window_handles[1])

        time.sleep(2)

        verify_otp(driver=_driver, hipi_otp=_hipi_otp)

        creater_list = ["everydaylifestyle", "123laughtergo"]

        for name in creater_list:
            follow_num = following(driver=_driver, creator_name=name)

        counter += 1

        print("Quiting the driver....") 
        _driver.quit()

        # Capture the end time and calculate the duration
        end_time = time.time()
        duration = end_time - start_time

        # Format the duration in minutes and seconds
        formatted_duration = time.strftime("%M:%S", time.gmtime(duration))

        print(f"Follow Done: {counter}, Time Taken: {formatted_duration} minutes\n")

        

    except IndexError:
        print("IndexError : List Exhausted")
        exit()

    except Exception as e:

        print(f"Error : {e}")
        print("Retiring the Proccess...")
        print()

        if usr_data:
            user_data_counter()

        _driver.quit()
        # continue
    #_driver.delete_all_cookies()
    

print(f"Counter : {counter}")



