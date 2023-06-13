from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb://localhost:27017"

# Connect to MongoDB
try:
    client = MongoClient(uri)
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Error connecting to MongoDB:", e)
    exit()

# Access a database
db = client["transfermarkt"]

# Access a collection
collection = db["players"]

# Perform a test operation
try:

    # Find documents
    documents = collection.find()
    for doc in documents:
        print(doc)
except Exception as e:
    print("Error performing MongoDB operation:", e)

# Close the connection
client.close()