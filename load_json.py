# This file was made for the CMPUT 291 Mini-Project 2 by Maheen Abbasi on March. 15, 2026

"""
This file will load the JSON dataset into the MongoDB via the following steps:
    1. Take JSON filename and port number from the command line input
    2. Connect to MongoDB and create a database called 291db
    3. Create a collection called furniture, and drop it if it already exists
    4. Insert the JSON data in batches, with the max. batch size of 100

It expects input in the following form: python load_json.py data.json port#
"""

# imports
import sys
import json
from pymongo import MongoClient

# Set max. batch size
BATCH = 100

# ----------------------------------------------------------------------------------------------------------------------- #
# DB Setup Functions
# ----------------------------------------------------------------------------------------------------------------------- #

"""
connect_db(port): takes a port and connects to the MongoDB server.

Input(s):
    port (int): The port number which the MongoDB server will run on

Returns:
    Database: A reference to the MongoDB db called '291db'
"""
def connect_db(port):
    # Create a client that connects to MongoDB on localhost, then access/create the db
    client = MongoClient("localhost", port)
    db = client["291db"]
    
    return db

"""
reset_collection(db): check if the 'furniture' collection exists, and drop it if found.

Input(s):
    db: The MongoDB databse

Returns:
    Collection: A reference to the 'furniture' colleciton
"""
def reset_collection(db):
    # Check if furniture collection already exists, and drop it if it does.
    if "furniture" in db.list_collection_names():
        db.drop_collection("furniture")
    
    return db["furniture"]

# ----------------------------------------------------------------------------------------------------------------------- #
# Loading
# ----------------------------------------------------------------------------------------------------------------------- #

"""
load(filename, collection): load furniture from a JSON file into a MongoDB

Steps:
    1. Read JSON file
    2. Convert each entry into a doc using the build_doc function
    3. Insert the doc into the MongoDB in batches

Input(s):
    filename (str): Path to the JSON file containing the furniture data
    collection (Collection): The MongoDB collection where the docs will be inserted

Returns:
    int: Total number of documents successfully inserted into the collection
"""
def load(filename, collection):
    # temp. list to store docs before batch insertion, and a counter for total inserrted docs
    batch = []
    total = 0

    # Open the JSON file and load its contents
    try:
        with open(filename, 'r', encoding = "utf-8") as f:
            data = json.load(f)

            # Proces each furniture item in the JSON file
            for item in data:
                # Convert each JSON entry
                doc = build_doc(item)
                batch.append(doc)

                # When batch size reaches the limit, insert into MongoDB
                if len(batch) == BATCH:
                    collection.insert_many(batch, ordered = False)
                    total += len(batch)
                    batch = []
                
            # Insert any remaining docs that didn't fill a full batch
            if batch:
                collection.insert_many(batch, ordered = False)
                total += len(batch)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        sys.exit(1)
        
    return total

# ----------------------------------------------------------------------------------------------------------------------- #
# Helper(s)
# ----------------------------------------------------------------------------------------------------------------------- #

"""
build_doc(item): helper function to convert a JSON furniture record into a MongoDB document.

Input(s):
    item (dict): A dict representing a furniture item from the JSON

Returns:
    dict: A dict formatted for insertion into the MongoDB 'furniture' colelciton
"""
def build_doc(item):
    # Built with the fields specified in the assignment
    return {
        "item_id": item.get("item_id"),
        "name": item.get("name"),
        "category": item.get("category"),
        "price": item.get("price"),
        "old_price": item.get("old_price"),
        "sellable_online": item.get("sellable_online"),
        "other_colors": item.get("other_colors"),
        "short_description": item.get("short_description"),
        "designer": item.get("designer"),
        "depth": item.get("depth"),
        "height": item.get("height"),
        "width": item.get("width"),
    }

# ----------------------------------------------------------------------------------------------------------------------- #
# Main
# ----------------------------------------------------------------------------------------------------------------------- #

def main():
    if len(sys.argv) != 3:
        print("Usage: python load_json.py <json_file> <port>")
        sys.exit(1)
    
    filename = sys.argv[1]
    port = int(sys.argv[2])

    db = connect_db(port)
    collection = reset_collection(db)

    count = load(filename, collection)

    print(f"{count} furniture items inserted successfully.")

if __name__ == "__main__":
    main()