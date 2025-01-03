import json
from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "real_estate_db"
COLLECTION_NAME = "properties"

def upload_to_mongo(json_file):
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    # Drop the collection if it exists
    db[COLLECTION_NAME].drop()
    
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Insert data into the collection
    db[COLLECTION_NAME].insert_many(data)
    print(f"Data successfully uploaded to {DATABASE_NAME}.{COLLECTION_NAME}")

if __name__ == "__main__":
    upload_to_mongo("data.json")
