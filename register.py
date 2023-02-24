import logging
# IMPORTING LOCAL "database.py" FILE AS MODULE
from constants import *
import database
import time

# <====================== VARIABLES ======================>
years = [19,20,21,22,23,24,25]
admin = [1387682420,1490833723,862799552,1339656586,1417818674]
# for y in database.results.list_collection_names():
#     # collectio name is "R19 Results" and we're slicing it like [1:3] ==> "19" 
#     # and then conveting to integer and appending that year to "years" list
#     years.append(int(y[1:3]))

student_registrations = {}
for y in years:
    # this dictionary cotains YEAR as a Key and its respective COLLECTION as a Value 
    # which is used to seggregate the registrations data YEAR-WISE
    student_registrations[y] = database.stu_registration[f'R{y} Student Registrations']
# <================================================================>

# <================== AUTHENTICATE USER ====================>

# This fuction is used to check whether the student is registered or not 
def authenticate_user(message):
    # print("Authenticating")
    registered = None
    # we'll check in every year's collection whether the student's chat-id
    # is registered or not. If we found the chat-id then we will break the loop 
    # and return "registered" variable as "True" else we will return "None"
    for y in years:
        if student_registrations[y].find_one({'_id':message.chat.id}) == registered:
            continue
        else:
            registered = True
            break
    return registered

# <=================================================================>

# <================== VERIFY SECURITY CODE AND REGISTER THE STUDENT ====================>

def verify_otp(message):
    if(message.text == otp_dict[message.chat.id][0]):
        mail_id = otp_dict.pop(message.chat.id)[1]
        roll_num = mail_id[0:10].upper()
        current_ids.append({
                "_id":message.chat.id,
                "ROLL_NUM":roll_num,
                "TIME": time.asctime(time.localtime())
                })
        if(mail_id[4:6].lower() == '5a'):
            year = str(int(mail_id[0:2]) - 1)
        else:
            year = mail_id[0:2]
        # Inserting the student details into the database
        student_registrations[int(year)].insert_many(current_ids)
        current_ids.clear()
        return True
    return False
# <=================================================================>

# <================== ADMIN AUTHENTICATION ====================>

def admin_authentication(message):
    if authenticate_user(message) and message.chat.id in admin:
        return True
    return False

# <=================================================================>

        
# <================== DELETE/ DEREGISTER THE USER(STUDENT) ====================>

def deleteUser(message):
    roll_num = message.upper()
    if(message[4:6].lower() == '5a'):
            year = str(int(message[0:2]) - 1)
    else:
        year = message[0:2]
    deleted_user = student_registrations[int(year)].find_one({"ROLL_NUM":roll_num})
    if deleted_user != None:
        student_registrations[int(year)].delete_one({"ROLL_NUM":roll_num})
    return deleted_user

# <=================================================================>

# <================== TOTAL REGISTRATION DATA ====================>

def total_registrations():
    no_of_registrations = ""
    for y in years:
        if student_registrations[y].find():
            registrations = list(student_registrations[y].find())
            no_of_registrations += f"{y}-Batch registrations: {len(registrations)}\n"
    return no_of_registrations
    
# <=================================================================>


# ====================== USER DETAILS =====================>

def user_details(message):
    details = ""
    roll_num = message.upper()
    if(message[4:6].lower() == '5a'):
            year = str(int(message[0:2]) - 1)
    else:
        year = message[0:2]
    details = student_registrations[int(year)].find_one({"ROLL_NUM":roll_num})
    if details != None:
        return dict(details)
    return details

# ====================================================>