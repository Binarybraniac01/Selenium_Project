# small functions that can be used for repetitive task
from UserNames.user_names_list import names_with_ages_gender
    

def get_name_age(func_name):
    with open("UserNames/last_used_number.txt", "r") as file:
        last_idx = file.read().strip()
        last_idx = int(last_idx)

    # Take the first element from the list
    name_age = names_with_ages_gender[last_idx]

    if func_name == "sign_up":
        with open("UserNames/last_used_number.txt", "w") as file:
            file.write(str(last_idx + 1))

    # Return the used name and age
    return name_age[0], name_age[1], name_age[2]
    
    
def user_data_counter():
    with open("UserNames/last_used_number.txt", "r") as f:
        stored_num = f.readline()
        
    with open("UserNames/last_used_number.txt", "w") as f:
        new_num = int(int(stored_num) - 1)
        
        f.write(str(new_num))
