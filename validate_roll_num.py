import logging
import re
# <==================== LOGGING ===========================>

reg_logger = logging.getLogger(__name__)
handler = logging.FileHandler("Error.log")
formatter = logging.Formatter("%(asctime)s - '%(name)s' - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
reg_logger.addHandler(handler)

# <=========================================================>

def valid_roll_num(message):
    roll_num_reg_exp=re.compile('\d{2}BQ+[1,5]A+(01|02|03|04|05|12|42|47|49|54|61)[0-9A-Za-z]\d')
    roll_number = (message.text).upper()
    matched_roll=re.match(roll_num_reg_exp,roll_number)
    if matched_roll != None and roll_number==str(matched_roll.group()):
        return True
    return False

# print(validate_roll_num("20bq1a42a3"))