# pip install pymongo
# mongoimport --db school_db --collection students --file /path/to/students.json
#    --jsonArray --host localhost --port 27017 --username <your_username> --password <your_password>
#    --authenticationDatabase admin

from pymongo import MongoClient, GEOSPHERE
from pprint import pprint

# Create the MongoDB client and connect to the database
client = MongoClient(host="localhost", port=27022, username="root", password="rootpassword")
study1 = client["study1"]  # Connect to the database "study1"

# Collection where geolocation data is stored
collection = study1['locations']

# Create a geospatial index on the "location" field
collection.create_index([("location", GEOSPHERE)])
print("Geospatial index created.")

# Insert documents with corrected location data (longitude, latitude)
locations = [
    {"name": "Park", "location": {"type": "Point", "coordinates": [-122.4194, 37.7749]}},  # San Francisco
    {"name": "Museum", "location": {"type": "Point", "coordinates": [-122.4094, 37.7849]}},  # Near San Francisco
    {"name": "Restaurant", "location": {"type": "Point", "coordinates": [-73.935242, 40.730610]}},  # New York
    {"name": "Library", "location": {"type": "Point", "coordinates": [-118.2437, 34.0522]}},  # Los Angeles
]

# Insert the location documents into the collection
collection.insert_many(locations)
print("Documents inserted with geolocation data.")

# Define the central point (San Francisco) and the search radius (5000 meters / 5 km)
san_francisco_location = [-122.4194, 37.7749]  # Longitude, Latitude
search_radius_meters = 5000  # 5 kilometers

# Perform a geospatial query to find locations within a 5 km radius of San Francisco
nearby_locations = collection.find({
    "location": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": san_francisco_location  # Longitude first, then latitude
            },
            "$maxDistance": search_radius_meters  # Search radius in meters
        }
    }
})

# Print the nearby locations
print("Nearby locations within 5 km radius of San Francisco:")
for location in nearby_locations:
    pprint(location)
