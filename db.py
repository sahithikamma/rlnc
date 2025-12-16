from pymongo import MongoClient


MONGO_URI = "mongodb+srv://rlncuser:rlnc12345@cluster0.paxzeab.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["rlnc_db"]

admin_col = db["admin"]
emp_col = db["employees"]
salary_col = db["salary"]
