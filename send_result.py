import logging
import database
import constants
import register as reg
# <==================== LOGGING ===========================>

reg_logger = logging.getLogger(__name__)
handler = logging.FileHandler("Error.log")
formatter = logging.Formatter("%(asctime)s - '%(name)s' - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
reg_logger.addHandler(handler)

# <=========================================================>

def result_message(message):
    # Initializing user Authorization dictionary
    authrization_dict = {}
    authrization_dict["message"] = "Please check the roll number. No results found!\nAny Problem? /help"
    authrization_dict["user_roll_num"] = None
    authrization_dict["user_id"] = None
    authrization_dict["id"] = None
    # Handling "message" object
    msg_list = message.text.split()
    Roll_no=msg_list[0].upper()
    year=Roll_no[:2]
    if Roll_no[4:6] == "5A":
        year=str(int(Roll_no[:2])-1)
    
    # Getting Collections from the database
    results_collection = database.results[f"R{year} Results"]
    reg_collection = database.stu_registration[f'R{year} Student Registrations']

    # Verifying the registration of the user
    user_dict = reg.results_authenticate_user(message)
    if user_dict == None:
        authrization_dict["message"] = constants.wrong_msg
        return authrization_dict
    user_dict = dict(user_dict)

    # Verifying the user with given roll number is registered or not
    user_of_given_roll_number = reg_collection.find_one({"ROLL_NUM":Roll_no})
    if user_of_given_roll_number == None:
        authrization_dict["message"] = "Unregistered student's result cannot be displayed!"
        return authrization_dict
    user_of_given_roll_number = dict(reg_collection.find_one({"ROLL_NUM":Roll_no}))

    # Updating the Authorization Dictionary by checking the current user is accessing his/her result or not
    if user_dict["_id"] != user_of_given_roll_number["_id"]:
        authrization_dict["id"] = user_of_given_roll_number["_id"]
        authrization_dict["user_roll_num"] = user_dict["ROLL_NUM"]
        authrization_dict["user_id"] = user_dict["_id"]
    
    # Result message generation begins here
    report = results_collection.find_one({"_id":Roll_no})
    if report == None:
        authrization_dict["message"] = f"Try checking your roll number.\n NOTE: You can only access Year-{year} Batch students results"
        return authrization_dict
    report_dict=dict(report)
    authrization_dict["message"] = "Roll Number: " + report_dict["_id"]+"\n"+"Name: "+report_dict["name"]+"\n"
    # PARTICULAR SEMESTER
    if len(msg_list) == 2:
        sem=msg_list[1]
        if(sem in report_dict.keys()):
            if len(report_dict[sem].items()) != 0:
                authrization_dict["message"] += f"➡️ {sem} Semester End Exam Result ⬅️\n"
                for j,k in report_dict[sem].items():
                    if j=="HTNO":
                        continue
                    authrization_dict["message"] += j+" : "+k+"\n"
                return authrization_dict
            authrization_dict["message"] = f"🔺️'{sem}' Semester End exam results are not available🔺️\nAny Problem? /help"
            return authrization_dict
        authrization_dict["message"] = "Please check the semester!\nAny Problem? /help"
        return authrization_dict

    # ALL SEMESTERS
    elif len(msg_list) == 1:
        for i in report_dict.keys():
            if i=="_id" or i=="name":
                continue
            else:
                if len(report_dict[i].items())!=0:
                    authrization_dict["message"] += f"\n ➡️ {i} Semester End Exam Result ⬅️\n"
                    for j,k in report_dict[i].items():
                        if j=="HTNO":
                            continue
                        authrization_dict["message"]+=j+" : "+str(k)+"\n"
        authrization_dict["message"] += "\nAny Problem? /help"
        return authrization_dict
    return authrization_dict

