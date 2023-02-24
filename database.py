# DATABASE CONNECTIVITY
import pymongo

# ESTABLISHING CONNECTION
client = pymongo.MongoClient("mongodb+srv://20bq1a4222:0URpI17aE6qph4sJ@restele-sample.kn66nzr.mongodb.net/test")

# ------------- VARIABLES THAT ARE USED TO ACCESS THE DATABASE --------------
# FOR STUDENT REGISTRATION 
stu_registration = client['Student_Registrations']
# FOR RESULTS
results = client["Results"]