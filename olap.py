import pandas as pd
from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Default MongoDB URL
db = client["real_estate_db"]  # Connect to the 'real_estate_db' database
collection = db["properties"]  # Connect to the 'properties' collection

# Step 2: Retrieve data from MongoDB and load it into a pandas DataFrame
data = list(collection.find({}))  # Retrieve all documents from the collection
df = pd.DataFrame(data)  # Convert the list of documents into a pandas DataFrame

# Optional: Print the first few records to inspect the data structure
print(df.head())

# ---- 1. Data Cleanup (Ensure Numeric Fields Are Correctly Formatted) ----
df['MIN_PRICE'] = pd.to_numeric(df['MIN_PRICE'], errors='coerce')  # Convert 'PRICE' to numeric, handle errors
df['BEDROOM_NUM'] = pd.to_numeric(df['BEDROOM_NUM'], errors='coerce')  # Convert 'BEDROOM_NUM' to numeric
df['BATHROOM_NUM'] = pd.to_numeric(df['BATHROOM_NUM'], errors='coerce')  # Convert 'BATHROOM_NUM' to numeric
df['CITY'] = df['CITY'].astype(str)  # Convert 'CITY' to string to avoid any issues during grouping

# Drop rows with NaN values in critical columns (optional)
df = df.dropna(subset=['MIN_PRICE', 'BEDROOM_NUM', 'BATHROOM_NUM', 'CITY', 'PROPERTY_TYPE'])

# ---- 2. Roll-up ----
# Aggregating PRICE by PROPERTY_TYPE (higher-level aggregation)
roll_up = df.groupby('PROPERTY_TYPE')['MIN_PRICE'].mean().reset_index()
print("\nRoll-up Example (Summarizing PRICE by PROPERTY_TYPE):")
print(roll_up)

# ---- 3. Drill-down ----
# Aggregating PRICE by CITY and LOCALITY (lower-level breakdown)
drill_down = df.groupby(['CITY', 'LOCALITY'])['MIN_PRICE'].mean().reset_index()
print("\nDrill-down Example (Breakdown by CITY and LOCALITY):")
print(drill_down)

# ---- 4. Dice ----
# Filtering data for Residential Apartments in Gurgaon (subset of data based on conditions)
dice = df[(df['CITY'] == 'Gurgaon') & (df['PROPERTY_TYPE'] == 'Residential Apartment')]
print("\nDice Example (Filtering data for Gurgaon and Residential Apartments):")
print(dice)

# ---- 5. Pivot ----
# Creating a pivot table to show the average PRICE by PROPERTY_TYPE and CITY
pivot = pd.pivot_table(df, values='MIN_PRICE', index='PROPERTY_TYPE', columns='CITY', aggfunc='mean', fill_value=0)
print("\nPivot Example (Average MIN_PRICE by PROPERTY_TYPE and CITY):")
print(pivot)

# Step 6: Close the MongoDB connection (optional)
client.close()