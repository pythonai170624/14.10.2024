# pip install pymongo
# mongoimport --db school_db --collection students --file /path/to/students.json
#    --jsonArray --host localhost --port 27017 --username <your_username> --password <your_password>
#    --authenticationDatabase admin

from pymongo import MongoClient

client = MongoClient(host="localhost", port= 27022, username="root", password="rootpassword")

study1 = client["study1"]  # db called study1

db_students = study1['students']  # collection called students

students = db_students.find()
# [ {}, {}, ...]
for one_student in students:
    print(one_student)
    # for key, value in one_student.items():
    #     print(key, type(key), str(value), type(value))


client.close()



