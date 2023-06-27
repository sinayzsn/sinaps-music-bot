from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# database
db = conn.database

# Created or Switched to collection names: my_gfg_collection
collection = db.my_gfg_collection