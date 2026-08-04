from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")
    
    # test connection
    client.admin.command("ping")

    print("MongoDB Connected Successfully!")

    db = client["DecisionTwinAI"]

    print("Database:", db.name)

except Exception as e:
    print("MongoDB Connection Failed:", e)