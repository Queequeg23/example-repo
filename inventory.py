
# ========Imports and Set Up=============================

# Import built-in modules for code and to enable automated env set-up
import sys
import subprocess
import re

# List of required packages to install
required_packages = ["tabulate", "pycountry"]

# Install packages and check for exception
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package]
        )

# Import country library and tabulate packages
import pycountry
import tabulate


# ========Class definitions==========
class Shoe():

    def __init__(self, country, code, product, cost, quantity):
        '''
        In this function initializes the following attributes for class Shoe:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        '''
        Return the cost of the shoes.

        Returns:
        cost(int) - the stored cost of an item
        '''
        return self.cost

    def get_quantity(self):
        '''
        Return the quantity of the shoes.

        Returns:
        quantity(int) - the stored quantity of an item
        '''
        return self.quantity

    def __str__(self):
        '''
        Returns a string representation of the Shoe class.
        '''
        stock_attributes = [
            f"Product country: {self.country}",
            f"Product code: {self.code}",
            f"Product name: {self.product}",
            f"Product cost: {self.cost:,}",
            f"Product quantity: {self.quantity:,}"
        ]
        return "\n".join(stock_attributes)


#=============Lists and sets============
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []

'''
Create set of valid countries from pycountries for input check.
'''
valid_countries = {country.name for country in pycountry.countries}


#==========Functions outside the class==============
def read_shoes_data(shoe_list):
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list.
    '''
    # Try-except loop to pick up file opening errors
    try:
        # open file, skip first line, iterate through file creating objects.
        with open("inventory.txt", "r") as inventory_file:
            inventory_file.readline()
            for record in inventory_file:
                # Strip new line markers, split at ','
                # and remove leading/ trailing blanks.
                attributes = [
                    attr.strip() for attr in record.strip().split(",")
                ]
                # Cast cost and quantity to integers
                for i in range(3, 5):
                    attributes[i] = int(attributes[i])

                # Create object with attributes from file
                shoe_list.append(Shoe(
                    attributes[0],
                    attributes[1],
                    attributes[2],
                    attributes[3],
                    attributes[4]
                    )
                )
        return shoe_list

    except FileNotFoundError:
        print(
            "File does not exist."
            "Please check inventory file is in the correct directory."
        )


def capture_shoes(shoe_list):
    '''
    This function allows a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object to the shoe list.
    '''
    # Although not required in brief additional functionality to
    # add object attributes to file was also added
    while True:
        print(
            "\nYou have chosen to enter information for a new product.\n"
            "\nPlease enter the product details as prompted. "
            "Or enter 0 to quit."
        )
        # Prompt for use inputs and check validity
        while True:
            country = input(
                "\nPlease enter the product country or 0 to quit: "
            ).title().strip()
            if country == "0":
                return
            elif country in valid_countries:
                break
            else:
                print("Invalid input. Please enter a valid country name.")

        while True:
            code = input(
                "\nPlease enter the product code or 0 to quit: "
            ).upper().strip()
            if code == "0":
                return
            elif re.fullmatch(r"[a-zA-Z]{3}\d{5}", code):
                break
            else:
                print(
                    "Invalid input. Code format should be"
                    " 3 alphabetic characters followed by 5 numbers."
                    "\nPlease enter a valid code.\n")

        while True:
            product = input(
                "\nPlease enter the product name or 0 to quit: "
            ).title().strip()
            if product == "0":
                return
            elif product and re.fullmatch(r"[a-zA-Z0-9 ]+", product):
                break
            else:
                print(
                    "Invalid input."
                    " Please use only characters, digits and blank spaces.\n"
                )
        while True:
            try:
                cost = int(input(
                    "\nPlease enter the product cost or 0 to quit: "
                    )
                )
                if cost == 0:
                    return
                elif cost < 0:
                    print(
                        "A cost less than zero not allowed. "
                        "Please enter a positive number."
                    )
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.\n")

        while True:
            try:
                quantity = int(input(
                    "\nPlease enter the product quantity or 0 to quit: "
                    )
                )
                if quantity == 0:
                    return
                elif quantity < 0:
                    print(
                        "A quantity of less than zero not allowed."
                        "Please enter a positive number."
                    )
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.\n")

        # Confirm inputs and prompt user to add to file
        while True:
            create_item = input(
                f"\nDo you wish to update file with this item?"
                f"\nProduct country: {country}"
                f"\nProduct code: {code}"
                f"\nProduct name: {product}"
                f"\nProduct cost: {cost:,}"
                f"\nProduct quantity: {quantity:,}"
                f"\n\nEnter Y/N "
            ).upper().strip()
            if create_item == "N":  # if N quit to main menu
                return
            elif create_item == "Y":  # if Y append list and write to file
                shoe_list.append(Shoe(country, code, product, cost, quantity))
                try:
                    with open("inventory.txt", "w") as inventory_file:
                        inventory_file.write(
                            "Country, Code, Product, Cost, Quantity\n"
                        )
                        for shoe in shoe_list:
                            inventory_file.write(
                                f"{shoe.country},  {shoe.code},"
                                f"  {shoe.product}, {shoe.cost},"
                                f" {shoe.quantity}\n"
                            )
                except FileNotFoundError:
                    print(
                        "File does not exist."
                        "Please check inventory file is in"
                        " the correct directory."
                    )
                print("\nFile successfully updated.")
                # Prompt to add another item
                while True:
                    add_item = input(
                        "\nDo you wish to add another item? Enter Y/N: "
                    ).upper().strip()
                    if add_item == "N":  # If N return to main menu
                        return
                    # If Y, break validation loop and continue
                    # with outer loop prompting for new item inputs
                    elif add_item == "Y":
                        break
                    else:
                        print("\nInvalid input. Please enter Y/N.")
                break
            else:
                print("\nInvalid input. Please enter Y/N.")


def view_all(shoe_list):
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function.
    '''
    # Convert object list to 2-D list of attributes
    shoe_matrix = [
        [
            shoe.country, shoe.code, shoe.product,
            f"{shoe.cost:,}", f"{shoe.quantity:,}"
        ]
        for shoe in shoe_list
    ]

    # Define column headers
    headers = [
        "Country", "Code", "Product", "Cost", "Quantity"
    ]

    # Print table
    print(tabulate.tabulate(shoe_matrix, headers=headers, tablefmt="rst"))


def re_stock(shoe_list):
    '''
    This function finds the shoe object with the lowest quantity.
    Prompts the user to ask if the item should be re-stocked,
    if re-stocking is required, shoe.quantity is incremented by the user
    defined amount and the file record updated.
    '''
    # Initialise update file flag to False
    update_file = False

    # Needs to account for the edge condition where more than one item has the
    # same minimum quantity.
    # Note: class defined function seems too much for this requirement,
    # but coded this way to meet requirements of the brief while still
    # accommodating possible edge conditions.

    # Identifies the lowest quantity attribute in the object list
    lowest_quantity = min(shoe_list, key=lambda x: x.get_quantity()).quantity
    # Creates list of objects with the lowest_quantity
    low_stock = [
        shoe for shoe in shoe_list if shoe.get_quantity() == lowest_quantity
    ]
    # Prints contents of low_stock list
    print("\nThe following items are low in stock.\n")
    for shoe in low_stock:
        print(shoe, end="\n\n")

    # Ask if user wishes to update any shoe.quantity in low_stock and increment
    for shoe in low_stock:
        while True:
            restock = input(
                f"Do you wish to restock {shoe.product}(Y/N)? "
            ).upper().strip()
            if restock == "Y":
                update_file = True
                # Ask for amount of quantity update and validate input
                while True:
                    try:
                        restock_quantity = int(input(
                            "\nHow many items to you wish to add? "
                            )
                        )
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                # Increment shoe.quantity input amount
                shoe.quantity += restock_quantity
                break
            elif restock == "N":
                break
            else:
                print("Invalid input. Please enter Y or N.\n")

    # If any shoe.quantity updated write updated list back to file
    if update_file:
        try:
            with open("inventory.txt", "w") as inventory_file:
                inventory_file.write(
                    "Country, Code, Product, Cost, Quantity\n"
                )
                for shoe in shoe_list:
                    inventory_file.write(
                        f"{shoe.country},  {shoe.code},  {shoe.product},"
                        f"{shoe.cost}, {shoe.quantity}\n"
                    )
        except FileNotFoundError:
            print(
                "File does not exist."
                "Please check inventory file is in the correct directory."
            )


def search_shoe(shoe_list):
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    # Prompt for user input and check validity.
    while True:
        search_term = input(
            "\nPlease enter item code for details you wish to retrieve. "
            "Or enter 0 to exit: "
            ).upper().strip()
        # If 0 return to main menu
        if search_term == "0":
            return
        # If blank or incorrect format prompt for correct format and try again
        elif not re.fullmatch(r"[A-Z]{3}\d{5}", search_term):
            print(
                "\nThe code you entered is not in the correct format.\n"
                "Product code should be 3 alphabetic "
                "characters followed by 5 numbers.\n"
            )
        # If correct format check for matches, assuming there may be duplicates
        # Build list of matches based upon search term
        else:
            matches = [shoe for shoe in shoe_list if shoe.code == search_term]
            for shoe in matches:
                print(shoe, end="\n\n")
                break
            # No matches found
            if not matches:
                print("\nThere are no items that match this code.")


def value_per_item(shoe_list):
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    # Need to use get_cost() and get_quantity()
    # Convert object list to 2-D list of attributes
    value_matrix = [
        [
            shoe.country,
            shoe.code,
            shoe.product,
            f"{shoe.cost:,}",
            f"{shoe.quantity:,}",
            f"{(shoe.quantity * shoe.cost):,}"
        ] for shoe in shoe_list
    ]
    value_headers = [
        "Country",
        "Code",
        "Product",
        "Cost",
        "Quantity",
        "Total value"
    ]
    print(
        tabulate.tabulate(value_matrix, headers=value_headers, tablefmt="rst")
    )


def highest_qty(shoe_list):
    '''
    Function determines the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # Return highest quantity variable
    highest_quantity = max(shoe_list, key=lambda x: x.get_quantity()).quantity
    # populate a temporary list with objects low in stock
    high_stock = [
        shoe for shoe in shoe_list
        if shoe.get_quantity() == highest_quantity
    ]
    print("The following items are recommended for sale.")
    for shoe in high_stock:
        print(shoe, end="\n\n")
    # think about how to format this?


#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''

print("\033[1;4m" + "\nInventory Management System\n" + "\033[0m")

read_shoes_data(shoe_list)

# Add conditional test for empty list, in which case only 1 is valid.
while True:
    print("\nPlease choose from the following options\n")

    print(
        "1. Add new inventory item.\n"
        "2. Display all inventory items.\n"
        "3. Restock items.\n"
        "4. Search for item using item code.\n"
        "5. Calculate and display inventory item values.\n"
        "6. Identify items for sale.\n"
        "0. Quit.\n"
    )

    try:
        menu_choice = int(input("Please enter your choice: "))

        if menu_choice == 1:
            capture_shoes(shoe_list)
        elif menu_choice == 2:
            view_all(shoe_list)
        elif menu_choice == 3:
            re_stock(shoe_list)
        elif menu_choice == 4:
            search_shoe(shoe_list)
        elif menu_choice == 5:
            value_per_item(shoe_list)
        elif menu_choice == 6:
            highest_qty(shoe_list)
        elif menu_choice == 0:
            sys.exit()
        else:
            print("Invalid input. Please enter a choice 1-6 or 0 to quit.")

    except ValueError:
        print("Invalid input. Please enter a choice 1-6 or 0 to quit.")
