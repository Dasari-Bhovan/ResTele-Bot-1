from dotenv import load_dotenv
import telebot
import logging
import os
# <=================== IMPORTING LOCAL MODULES =================>
from validate_roll_num import *
from constants import *
import register as reg
import send_result
import send_otp
# <================================================================>

# <==================== STATICS ===========================>
log_message = "%(asctime)s\n - '%(name)s' - %(levelname)s - %(message)s\n================================================================"
logging.basicConfig(level=logging.INFO, filemode="a", filename='Error.log',format=log_message)
load_dotenv() # Loading the environment variables

# <=========================================================>

# <======================= MAIN FUNCTION ============================>
while True:
    # ================== BODY OF THE CODE =================>
    # Creating the Bot instance
    bot = telebot.TeleBot(os.getenv('API_KEY_TEST'))
    try:
        # ================== START COMMAND =================>
        @bot.message_handler(commands=['start'])
        def start(message):
            if reg.authenticate_user(message):
                bot.send_message(message.chat.id, start_msg)
            else:
                bot.send_message(message.chat.id, auth_msg)
        # ====================================================>

        # ================== HELP COMMAND ====================>
        @bot.message_handler(commands=['help'])
        def help(message):
            bot.send_message(message.chat.id, help_msg)
        # ====================================================>

        # ================== REGISTER COMMAND =================>
        @bot.message_handler(commands=['register'])
        def register(message):
            if reg.authenticate_user(message) == None:
                bot.send_message(message.chat.id, "Enter Your Email to get registered")
                bot.register_next_step_handler(message, getMailId)
            else:
                bot.send_message(message.chat.id, "You've already registered.\nEnter roll number to view results")
        # TO GET MAIL ID AND VERIFY IT
        def getMailId(message):
            mailid = (message.text).lower()
            if (len(mailid) == 19) and (('bq1a' in mailid) or ('bq5a' in mailid))  and ('@vvit.net' in mailid):
                name = 'VVITIAN'
                if(message.chat.first_name and message.chat.last_name):
                    name = message.chat.first_name+ " " + message.chat.last_name
                # OTP GENERATION FUNCTION CALL
                bot.send_message(message.chat.id, "Please wait..!")
                if(send_otp.otpmail(message, name)):
                    bot.send_message(message.chat.id, "Verification code is sent to your mail Successfully!")
                    bot.send_message(message.chat.id, "Please enter the 6-digit code")
                    bot.register_next_step_handler(message, otpverification)
                else:
                    bot.send_message(message.chat.id, "Something went wrong! Enter mail-id again")
                    bot.register_next_step_handler(message, getMailId)
            else:
                bot.send_message(message.chat.id, "Invalid Email-id.")
                bot.send_message(message.chat.id, "Enter Email-id again \nAny Problem? /help")
                bot.register_next_step_handler(message, getMailId)
        # TO VERIFY OTP
        def otpverification(message):
            if(reg.verify_otp(message)):
                bot.send_message(message.chat.id, "You've successfully registered")
                bot.send_message(message.chat.id, "Enter roll number to view results")
            else:
                otp_dict[message.chat.id][2] -= 1
                if(otp_dict[message.chat.id][2] == 0):
                    bot.send_message(message.chat.id, "Code Mismatched!\n You have 0 tries left.")
                    bot.send_message(message.chat.id, "Enter your mail-id again \nAny Problem? /help")
                    bot.register_next_step_handler(message, getMailId)
                else:
                    bot.send_message(message.chat.id, f"Code Mismatched!\nYou have {otp_dict[message.chat.id][2]} tries left. Please enter carefully")
                    bot.register_next_step_handler(message,otpverification)
        # ====================================================>

        # ====================== DEREGISTER USER COMMAND =====================>
        @bot.message_handler(commands=["deleteuser"], func=reg.admin_authentication)
        def get_delete_user(message):
            bot.send_message(message.chat.id, "Enter the student Roll Number")
            bot.register_next_step_handler(message, delete_user)

        def delete_user(message):
            try:
                bot.send_message(message.chat.id, str(reg.deleteUser(message.text)))
            except Exception as e:
                bot.send_message(message.chat.id,)
        # ====================================================>

        # ====================== USER DETAILS COMMAND ===================>
        @bot.message_handler(commands=["finduser"], func=reg.admin_authentication)
        def get_user_details(message):
            bot.send_message(message.chat.id, "Enter the student Roll Number")
            bot.register_next_step_handler(message, user_details)

        def user_details(message):
            bot.send_message(message.chat.id, str(reg.user_details(message.text)))
        # ====================================================>

        # ====================== SEND REGISTRATION DATA =====================>
        @bot.message_handler(commands=["totalregistrations"], func=reg.admin_authentication)
        def total_registerd(message):
            bot.send_message(message.chat.id, reg.total_registrations())
        # ====================================================>
        
        # ====================== RESULTS =====================>
        def validate_roll_number(message):
            if(reg.authenticate_user(message)):
                if valid_roll_num(message):
                    return True
                bot.send_message(message.chat.id, wrong_msg)
                return False
            bot.send_message(message.chat.id, auth_msg)
            return False

        @bot.message_handler(func=validate_roll_number)
        def msg_result(message):
            result = send_result.result_message(message)
            if result['user_roll_num'] == None and result["id"] == None:
                bot.send_message(message.chat.id, result["message"]+"\n" + report)
            elif result['user_id'] not in reg.admin:
                bot.send_message(result["id"], f'Student with {result["user_roll_num"]} has accessed your results.')
                bot.send_message(result["user_id"], result["message"]+"\n" + report)
            else:
                bot.send_message(result["user_id"], result["message"]+"\n" + report)
        # ====================================================>

        # ====================== POLLING =====================>
        bot.polling(non_stop=True, timeout=30)
        # ====================================================>
    except Exception as e:
        logging.exception(reg.total_registrations()+str(e), exc_info=True)
        bot.stop_polling()