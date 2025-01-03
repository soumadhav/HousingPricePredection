import json
from pymongo import MongoClient
import certifi


# Configure MongoDB Atlas connection 
MONGO_URI = "mongodb+srv://housing:housing_password@soumyamongo1.8eq0f.mongodb.net/?retryWrites=true&w=majority&appName=soumyaMongo1"
DATABASE_NAME = "housing_db"
COLLECTION_NAME = "property_sales"


# Read Json file and upload to mongo atlas, delete db if already exists.
def upload_to_mongo(json_file):
    # Connect to MongoDB Atlas
    client =  MongoClient(MONGO_URI, tlsCAFile=certifi.where()) # MongoClient(MONGO_URI)
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
    upload_to_mongo("melbourne_housing.json")
