from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["real_estate_db"]
collection = db["properties"]

# Slice operation: Filter properties by 'CITY'
city = 'Gurgaon'
slice_data = list(collection.aggregate([
    {"$match": {"CITY": city}},  # Filter properties in a specific city
    {"$project": {"PROP_ID": 1, "MIN_PRICE": 1, "PROPERTY_TYPE": 1, "CITY": 1}}  # Select necessary fields
]))

print(slice_data)
