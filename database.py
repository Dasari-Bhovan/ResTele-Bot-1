# DATABASE CONNECTIVITY
import pymongo

# ESTABLISHING CONNECTION
client = pymongo.MongoClient("mongodb://localhost:27017")

# ------------- VARIABLES THAT ARE USED TO ACCESS THE DATABASE --------------
# FOR STUDENT REGISTRATION 
stu_registration = client['Student_Registrations']
# FOR RESULTS #
results = client["Results"]