from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["real_estate_db"]
collection = db["properties"]

# Aggregate the data
pipeline = [
    {
        "$group": {
            "_id": None,
            "total_price": {"$sum": "$MIN_PRICE"},  # Summing the total price of all properties
            "avg_price_per_sqft": {"$avg": "$PRICE_SQFT"}  # Average price per sqft
        }
    }
]

result = collection.aggregate(pipeline)

# Output the result
for item in result:
    print(f"Total Price: {item['total_price']}, Avg Price per Sqft: {item['avg_price_per_sqft']}")
