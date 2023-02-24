import os
import math
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
from constants import otp_dict

current_email = [os.getenv("my_email")]
i = [0]
password_list = [os.getenv("password")]
print(current_email, password_list)

def generateOtp():
    digits="0123456789"
    OTP=""
    for i in range(6) :
        OTP+= digits[math.floor(random.random() * 10)]
    return OTP

# OTP GENERATION AND SENDING IT TO THEIR COLLEGE MAIL-IDS
def otpmail(mailid, name):
    # print(mailid.text)
    # print(1)
    try:
        my_email = current_email[0]
        print(my_email)
        password = password_list[0]
        # print(1)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "OTP for VVIT Results Bot"
        msg['From'] = current_email[0]
        otp = []
        otp = generateOtp()
        otp_dict.update({mailid.chat.id:[otp,mailid.text,3]})
        # print(otp_dict)
        x="""
        <html>
        <body>
        <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
        <div style="margin:50px auto;width:70%;padding:20px 0">
            <div style="border-bottom:1px solid #eee">
            <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">VVIT RESULTS BOT</a>
            </div>
            <p style="font-size:1.1em">Hi """ + name + """,</p>
            <p> Use the following OTP to complete your Registration</p>
            <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">"""+otp+"""</h2>
            <p style="font-size:0.9em;">Regards,<br />VVIT MANAGEMENT<if(generateOtp() not in OTP):
            OTP.append(otp)/p>
            <hr style="border:none;border-top:1px solid #eee" />
            <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
            <p>VVIT</p>
            </div>
        </div>
        </div>
        </body>
        </html>
        """
        parthtml=MIMEText(x,'html')
        msg.attach(parthtml)
        connection=smtplib.SMTP("smtp.gmail.com", port=587)
        connection.ehlo()
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(my_email,mailid.text,msg.as_string())
        connection.quit()
    except Exception as e:
        print(e)
        return False
    else:
        return True
