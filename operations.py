"""
This file handles operations on the document store, including:
    1. Discount check
    2. Keyword-match search
    3. Category-based search
    4. Adding to the db
"""

# Imports
import sys
from pymongo import MongoClient
import shutil

"""
connect_db(): establish a connection to the db
"""
def connect_db(port):
    client = MongoClient("localhost", port)
    return client["291db"]["furniture"]

"""
menu(): self-explanatory
"""
def menu():
    print()
    center_print("ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ")
    center_print("➳♥ ----- Furniture db ----- ➳♥")
    center_print("ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ")
    print()
    center_print("1. Discount Check")
    center_print("2. Keyword Search")
    center_print("3. Category Search")
    center_print("4. Add Furniture")
    center_print("5. Exit")

# ----------------------------------------------------------------------------- #
# Functions
# ----------------------------------------------------------------------------- #

"""
discount_check(): Function to check if a furniture item is on discount. It:
    
    1. Prompts the user to input the EXACT furniture name
    2. Searches the collection for the furniture
    3. Returns the furniture info (if only one item was found), or a list to choose from
    if several items were found with the same name given. Global pagination is followed.

Input: collection
Output: Furniture info output on terminal
"""
def discount_check(collection):
    # USer input
    name = input("\n❁›--› Please enter the exact furniture name: ")

    # Find all items with the name given above
    items = list(collection.find({"name": name}))

    # Case 1: No items found -> give the message
    if not items:
        print()
        center_print("🚫 No furniture found with that name 🚫")
        input("\n❁›--› Press any button to continue.")
        return
    
    # Case 2: Multiple items found -> let user choose by item_id
    if len(items) > 1:
        # Show the items
        print("\n╰┈➤ Multiple items found:\n")
        
        selected = paginate_list(items)

        if selected is None:
            print()
            center_print("🚫 Cancelled 🚫")
            return

    # Case 3: One item found -> default to choosing that, which should be the first in the list
    else:
        selected = items[0]
    
    # CHeck the discount
    price = selected.get("price")
    old_price = selected.get("old_price")

    # Handle None for either case (just in case it happens)
    if old_price is not None and price is not None and old_price > price:
        print()
        center_print("✅ Item is on discount ✅")
        print()
        center_divider()
        center_print(f"Name: {selected.get('name')}")
        center_print(f"Category: {selected.get('category')}")
        center_print(f"Price: {price}")
        center_divider()
        input("\n❁›--› Press any button to continue.")
    else:
        print()
        center_print("🚫 This furniture is not on discount 🚫")
        input("\n❁›--› Press any button to continue.")

"""
keyword_search(): Function to allow the user to search for furniture items based on a keyword they provide. It:
    
    1. Prompts the user for input, expecting a keyword (NOT a substring)
    2. Searches the collection for matching furniture items and displays a paginated list

Input: collection
Output: Paginated list of matching furniture items, if applicable. Error/Not Found messages otherwise.
"""
def keyword_search(collection):
     while True:
        #take input keyword from user to match with the keyword (case-sensitive)
        while True:
            keyword = input("\n❁›--› Please enter a keyword ['b' to return]: ").strip()
            if keyword.lower() == "b":
                return
            result = list(collection.find({"name":{"$regex": f"\\b{keyword}\\b", "$options": ""}},{"name":1,"category":1,"price":1,"short_description":1}))
            
            if not result:
                print()
                center_print("🚫 No furniture found with that keyword 🚫")
                input("\n❁›--› Press any button to continue.")
            else:
                break

        page = 0
        page_size = 5
        total_pages = (len(result) - 1) // page_size + 1

        while True:
            start = page * page_size
            end = start + page_size

            print()
            center_print("☆彡 ----- Items ----- ☆彡")

            # Show the current page items
            for i, item in enumerate(result[start:end], start=start + 1):
                center_print(f"{i}. Name: {item['name']} | Category: {item['category']} | Price: ${item['price']:.2f}")
                print()
                center_print(f"    Description: {item['short_description']}")
                print()
            center_print("☆彡 ----- END PAGE ----- ☆彡")


            if page < total_pages - 1:
                print("❁ N. Next page")
            if page > 0:
                print("❁ P. Previous page")
            print("❁ B. Back")
            print("❁ M. Back to main menu")

            choice = input("\n❁›--› Please choose an option: ").strip().lower()

            # Got to the next page
            if choice == "n" and page < total_pages - 1:
                page += 1

            # Go to the previous page
            elif choice == "p" and page > 0:
                page -= 1

            # Go back to keyword input
            elif choice == "b":
                break
            
            # go to main menu
            elif choice == "m":
                return  

"""
category_search: Function to allow the user to view existing categories from 
the furniture collection, and view specific items within those collections. It:

    1. Displays a paginated list of all categories from the current furniture db
    2. Allows the user to choose a category, and display a paginated list of items within that category
    3. Allows the user to choose a speciifc item from the above list, and view specific furniture info

Input: collection
Output: Various terminal output based on user input/choices
"""
def category_search(collection):

    # display category list for the user to choose from
    categories = collection.distinct("category")

    page = 0
    page_size = 5
    total_pages = (len(categories)-1)//page_size +1
    
    while True:
        start = page * page_size
        end = start + page_size

        print()
        center_print("☆彡 ----- Categories ----- ☆彡")

        # Show the current page items
        for i, item in enumerate(categories[start:end], start=start + 1):
            center_print(f"{i}. {item}")
        print()
        center_print("☆彡 ----- END PAGE ----- ☆彡")

        if page < total_pages - 1:
            print("❁ N. Next page")
        if page > 0:
            print("❁ P. Previous page")
        print("❁ B. Back")
        print("❁ [number] Select a category")

        user_input = input("\n❁›--› Please choose an option: ").strip() 

        # Go to the next page
        if user_input.lower() == "n" and page < total_pages - 1:
            page += 1

        # Go to the previous page
        elif user_input.lower() == "p" and page > 0:
            page -= 1

        # Go back to the homepage
        elif user_input.lower() == "b":
            return None
        
        else:
            try:
                num = int(user_input)
                if 1<= num <=len(categories):
                    user_input = categories[num-1]
                    break
                else:
                    center_print("🚫 Invalid number, try again 🚫")
            except ValueError:
                center_print("🚫 Please enter a valid option 🚫")

    # items in chosen category
    result = list(collection.find({"category": user_input},{"name":1,"item_id":1,"price":1}).sort("price",-1))

    if not result:
        center_print("🚫 No item available in this category 🚫")
        input("\n❁›--› Press any button to continue.")
    else:

        page = 0
        page_size = 5
        total_pages = (len(result)-1)//page_size + 1
        
        while True:

            start = page * page_size
            end = start + page_size

            print()
            center_print("☆彡 ----- Items ----- ☆彡")

            # Show the current page items
            for i, item in enumerate(result[start:end], start=start + 1):
                center_print(f"{i}. Name: {item['name']} | ID: {item['item_id']} | Price: ${item['price']:.2f}")
            print()
            center_print("☆彡 ----- END PAGE ----- ☆彡")

            if page < total_pages - 1:
                print("❁ N. Next page")
            if page > 0:
                print("❁ P. Previous page")
            print("❁ B. Back")
            print("❁ [number] Select an item") 

            choice = input("\n❁›--› Please choose an option: ").strip().lower()

            # Go to the next page
            if choice == "n" and page < total_pages - 1:
                page += 1

            # Go to the previous page
            elif choice == "p" and page > 0:
                page -= 1

            # Go back to the homepage
            elif choice == "b":
                return None
            
            else:
                try:
                    num = int(choice)

                    # Only allow numbers shown on the current oage
                    if start + 1 <= num <= start + len(result[start:end]):
                            selected = result[num - 1]
                            item = collection.find_one({"item_id":selected["item_id"]})
                            print()
                            center_divider()
                            center_print(f"Name: {item['name']}")
                            center_print(f"Category: {item['category']}")
                            center_print(f"Price: ${item['price']:.2f}")
                            center_print(f"Description: {item['short_description']}")
                            center_print(f"Designer: {item['designer']}")
                            center_divider()
                            input("\n❁›--› Press any button to continue.")
                    else:
                        center_print("🚫 Invalid selection 🚫")
                except ValueError:
                     center_print("🚫 Invalid selection 🚫") 

"""
add_furniture(): Function to allow the user to add a furniture item to the collection by providing furniture ID, Name, Price, Category, 
a short description, and the designer of the item.

Input: collection
Output: Various terminal output depending on user input and results of adding furniture.
"""
def add_furniture(collection):

    # prompt user for furniture details 
    new_id = str(input("\nPlease enter the ID for the new furniture item: ").strip())
    if not new_id:
        print()
        center_print("🚫 Item ID cannot be empty 🚫")
        return

    # Check if item_id already exists
    id_exists = collection.find_one({"item_id": new_id})
    if id_exists:
        print()
        center_print("🚫 This furniture item ID already exists 🚫")
        return

    new_name = input("Please enter the name of the new furniture item: ").strip()
    if not new_name:
        print()
        center_print("🚫 Name cannot be empty 🚫")
        return

    new_price = input("Please enter the price of the new furniture item: ").strip()
    try:
        new_price = float(new_price)
    except ValueError:
        print()
        center_print("🚫 Price must be a number 🚫")
        return

    new_category = input("Please enter the item's category: ").strip()
    if not new_category:
        print()
        center_print("🚫 Category cannot be empty 🚫")
        return

    new_description = input("Please enter a short description of the item: ").strip()
    if not new_description:
        print()
        center_print("🚫 Short description cannot be empty 🚫")
        return

    new_designer = input("Please enter the item's designer: ").strip()
    if not new_designer:
        print()
        center_print("🚫 Designer cannot be empty 🚫")
        return
    # enter the new item into the collections
    # new furniture
    new_furniture = {
        "item_id": new_id,
        "name": new_name,
        "category": new_category,
        "price": new_price,
        "old_price": None,
        "sellable_online": None,
        "other_colors": None,
        "short_description": new_description,
        "designer": new_designer,
        "depth": None,
        "height": None,
        "width": None
    }
    try:
        collection.insert_one(new_furniture)
        print()
        center_print("✅ Furniture item added successfully ✅")
        input("\n❁›--› Press any button to continue.")
    except Exception:
        print()
        center_print("🚫 Failed to add furniture item 🚫")

# ----------------------------------------------------------------------------- #
# Helpers
# ----------------------------------------------------------------------------- #

"""
Helper function to help center the terminal output so the tables look nicer, using shutil
-> keep in mind that it CANNOT support newlines, so use print() before or after center_print() or store lines[] and then do center_print(lines)
"""
def center_print(text = ""):
    width = shutil.get_terminal_size().columns
    print(text.center(width))

"""
Resueable center divider
"""
def center_divider(pattern = "--❁", repeat = 15):
    width = shutil.get_terminal_size().columns
    line = pattern * repeat
    print(line.center(width))

"""
Paginate a list of items
"""
def paginate_list(items, page_size=5):
    page = 0
    total_pages = (len(items) - 1) // page_size + 1

    while True:
        start = page * page_size
        end = start + page_size

        print()
        center_print("☆彡 ----- Items ----- ☆彡")

        # Show the current page items
        for i, item in enumerate(items[start:end], start=start + 1):
            center_print(f"{i} | {item['name']} | ${item['price']:.2f}")
        print()
        center_print("☆彡 ----- END PAGE ----- ☆彡")

        # Navigation options
        print("Options:\n")
        print("❁ [number] Select item")
        if page < total_pages - 1:
            print("❁ N. Next page")
        if page > 0:
            print("❁ P. Previous page")
        print("❁ B. Back")

        choice = input("\n❁›--› Please choose an option: ").strip().lower()

        # Got to the next page
        if choice == "n" and page < total_pages - 1:
            page += 1

        # Go to the previous page
        elif choice == "p" and page > 0:
            page -= 1

        # Go back to the homepage
        elif choice == "b":
            return None

        # Select an item
        else:
            try:
                num = int(choice)
                if 1 <= num <= len(items):
                    return items[num - 1]
                else:
                    center_print("🚫 Invalid selection 🚫")
            except ValueError:
                center_print("🚫 Invalid input 🚫")

# ----------------------------------------------------------------------------- #
# Main
# ----------------------------------------------------------------------------- #

"""
main()
"""
def main():
    if len(sys.argv) != 2:
        print("Usage: python furniture_app.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    collection = connect_db(port)

    while True:
        menu()
        choice = input("\n❁›--› Please choose an option (1-5): ")

        if choice == "1":
            discount_check(collection)

        elif choice == "2":
            keyword_search(collection)

        elif choice == "3":
            category_search(collection)

        elif choice == "4":
            add_furniture(collection)

        elif choice == "5":
            print("\nExiting...\n")
            break

        else:
            print("\nInvalid option")

if __name__ == "__main__":
    main()
