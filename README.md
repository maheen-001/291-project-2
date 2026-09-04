# CMPUT 291 Project 2 – Furniture Database System

A command-line furniture management system built using **Python** and **MongoDB**.

The system uses a MongoDB database to store IKEA furniture data and allows users to search, browse, check discounts, and add furniture items.

## Team Members

* Maheen Abbasi
* Manaal Naeem
* Harnoor Tihar

## Features

* Load furniture data from a JSON file into MongoDB
* Search for furniture by name
* Browse furniture by category
* Check whether a furniture item is on discount
* Add new furniture items
* Paginate search results
* Format results for the command line

## Technologies

* Python
* MongoDB
* MongoDB Query Language
* JSON

## Project Structure

```text
load_json.py      # Loads JSON furniture data into MongoDB
operations.py     # Main furniture database interface
```

## Running the Program

### 1. Load the data

```bash
python3 load_json.py <data> <port>
```

Replace `<data>` with the path to the JSON data file and `<port>` with the port MongoDB is running on.

Example:

```bash
python load_json.py data/sample_2000.json 27017
```

### 2. Run the application

```bash
python3 operations.py <port>
```

Example:

```bash
python operations.py 27017
```

> On Windows, `python` can be used instead of `python3`.

## Available Operations

### Discount Check

Check whether a specific furniture item is currently on discount.

### Keyword Search

Search for furniture by name. Searches are case-sensitive and require an exact name match.

### Category Search

Browse all furniture items belonging to a selected category.

### Add Furniture

Add a new furniture item to the database by providing its required information.

### Exit

Exit the application.

## Database

The project creates a MongoDB database named `291db` with a `furniture` collection. Furniture data is loaded from a JSON file during the initial setup.

## Collaboration

We did not collaborate with anyone outside of the project group.

---

**CMPUT 291 – Winter 2026**
**University of Alberta**
