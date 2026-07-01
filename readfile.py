import pandas as pd
from pymongo import MongoClient

# Step 1: Load your dataset (CSV format in this case)
# Replace 'your_dataset.csv' with the path to your downloaded Kaggle dataset
df = pd.read_csv('gurgaon_10k.csv')

# Step 2: Connect to MongoDB server
client = MongoClient("mongodb://localhost:27017/")  # Default MongoDB URL
db = client["real_estate_db"]  # Create or connect to the database 'real_estate_db'
collection = db["properties"]  # Create or connect to the 'properties' collection

# Step 3: Convert the dataframe to a list of dictionaries (each row becomes a document)
data_dict = df.to_dict("records")

# Step 4: Insert data into the MongoDB collection
collection.insert_many(data_dict)

print("Data imported successfully!")

# Step 5: Close the connection (optional)
client.close()
