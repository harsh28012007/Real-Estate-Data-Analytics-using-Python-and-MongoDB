from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # MongoDB URI
db = client["real_estate_db"]  # Your database name
collection = db["properties"]  # Your collection name

# Extract all documents from the collection
data = collection.find({})  # Find all documents in the collection

# Convert to a list (you can also directly process the cursor if needed)
data_list = list(data)

#transform

# Example of transformation (cleaning, adding a calculated field)
for record in data_list:
    # Add a new field price_per_area if 'SUPERBUILTUP_SQFT' and 'MIN_PRICE' are present
    if 'SUPERBUILTUP_SQFT' in record and 'MIN_PRICE' in record:
        super_built_up_sqft = record['SUPERBUILTUP_SQFT']
        min_price = record['MIN_PRICE']
        
        if super_built_up_sqft and super_built_up_sqft != "NaN":
            price_per_area = min_price / super_built_up_sqft
            record['price_per_area'] = price_per_area
        else:
            record['price_per_area'] = None
    else:
        record['price_per_area'] = None


    # Filter out records that don't have necessary fields like 'MIN_PRICE' or 'SUPERBUILTUP_SQFT'
    if not (record.get('MIN_PRICE') and record.get('SUPERBUILTUP_SQFT')):
        data_list.remove(record)  # Optionally remove invalid records

# After transformation, data_list will have the cleaned and transformed data

#load

# Assuming we want to load the transformed data back into MongoDB in a new collection
transformed_collection = db["res_properties"]  # New collection for transformed data

# Insert transformed data
transformed_collection.insert_many(data_list)