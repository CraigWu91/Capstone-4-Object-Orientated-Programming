# Requires tabulate module used in view_all function
from tabulate import tabulate

# Create a class to initialise attributes and create methods
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    def get_cost(self):
        return self.cost
   
    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f'''
        {self.country}
        {self.code}
        {self.product}
        {self.cost}
        {self.quantity}
        '''
# Create empty list to store the data in inventory text file
shoe_list = []

# Function to read from text file and store in list
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as f:
            next(f)
            for lines in f:
                data = lines.strip().split(",")
                shoe = Shoe(data[0], data[1], data[2], float(data[3]), int(data[4]))
                shoe_list.append(shoe)
    except FileNotFoundError:
        print("inventory.txt not found")

# Function to add new item to list and text file
def capture_shoes():
    while True:
        try:
            country = input("Country: ")
            code = input("code: ")
            product = input("product: ")
            cost = float(input("Cost: "))
            quantity = int(input("Quantity: "))
            shoe = Shoe(country, code, product, cost, quantity)
            shoe_list.append(shoe)
            with open("inventory.txt", "a") as f:
                f.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")
            print("Item successfully added")
            break
        except ValueError:
            print("Incorrect data type, please try again")

# Function to iterate through list and tabulate for nice display
def view_all():
    table = []
    for shoe in shoe_list:
        row = [shoe.country, shoe.code, shoe.product, shoe.cost, int(shoe.quantity)]
        table.append(row)
    print(tabulate(table, headers=['Country', 'Code', 'Product', 'Cost', 'Quantity'], tablefmt='grid'))

# Function to find item with lowest quantity and add to it
def re_stock():
    try:
        while True:
            min_qty = min(shoe_list, key=lambda x: int(x.quantity))
            print(f"The {min_qty.product} shoe has the lowest quantity of {min_qty.quantity}")
            restock = input("Would you like to add more shoes to the stock? Type y for yes or n for no: ").lower()
            if restock == "y":
                new_qty = int(input("Enter the quantity of shoes to add: "))
                min_qty.quantity += int(new_qty)
                with open("inventory.txt", "r+") as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        data = line.strip().split(",")
                        if data[1] == min_qty.code:
                            data[4] = str(min_qty.quantity)
                            line = ','.join(data) + '\n'
                        f.write(line)
                    f.truncate()
                print(f"{new_qty} shoe ('s) added to the {min_qty.product} stock")
            elif restock == "n":
                break
            else:
                print("incorrect option entered, please try again")
    except ValueError:
        print("Incorrect data type entered, please try again")

# Find item in list and print it
def search_shoe():
    code = input("Enter the shoe code: ")
    for shoe in shoe_list:
        if shoe.code == code:
            print(f'''
            Country: {shoe.country}
            Code: {shoe.code}
            Product: {shoe.product}
            Cost: {shoe.cost}
            Quantity: {shoe.quantity}
            ''')
            break
    else:
        print("Shoe not found")

# Create a table with total value of items
def value_per_item():
    table = []
    for shoe in shoe_list:
        value = float(shoe.cost) * float(shoe.quantity)
        row = [shoe.code, shoe.product, value]
        table.append(row)
    print(tabulate(table, headers=['Code', 'Product', 'Value'], tablefmt='grid'))

# Sort list item with highest quantity in descending and print the first
def highest_qty():
    sorted_list = sorted(shoe_list, key=lambda x: x.quantity, reverse=True)
    shoe = sorted_list[0]
    print(f"The {shoe.product} shoe has the highest quantity of {shoe.quantity} and should be on sale")

# Logic for the program
read_shoes_data()
while True:
    menu = input('''
    Please select from the menu:
    1) Capture new shoe
    2) View all stock
    3) Restock
    4) Search via code
    5) Calculate total value of each item
    6) View highest quantity
    7) Exit\n''')
    if menu == "1":
        capture_shoes()

    elif menu == "2":
        view_all()

    elif menu == "3":
        view_all()
        re_stock()

    elif menu == "4":
        search_shoe()

    elif menu == "5":
        value_per_item()

    elif menu == "6":
        highest_qty()

    elif menu == "7":
        exit()

    else:
        print("Please select appropriate menu option")