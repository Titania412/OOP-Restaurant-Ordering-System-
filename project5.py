import csv

"""Represents a single item on the restaurant menu."""
class MenuItem:
    def __init__(self, name, price, category, sizes = None):

        self.name = name
        self.price = float(price)
        self.category = category
        self.sizes = sizes

    def get_price(self, size = "medium"):
        if self.sizes is None:
            return self.price

        return self.price + self.sizes[size]

    def __str__(self):
        return self.name + " - $" + str(self.price)

"""Holds all menu items, organized by category."""
class Menu:
    def __init__(self):
        # Each category stores a list of MenuItem objects
        self.categories = {
            "Appetizers": [],
            "Entrees": [],
            "Desserts": [],
            "Beverages": []
        }

    def add_item(self, item: MenuItem):
        self.categories[item.category].append(item)

    def show_category(self, category_name):
        print("\n" + category_name + ":")

        num = 1
        for item in self.categories[category_name]:
            print(str(num) + ".) " + str(item))
            num += 1

    def get_item_by_number(self, category_name, number):
        return self.categories[category_name][number - 1]

"""Represents a selected item in the customer's order."""
class OrderItem:
    def __init__(self, menu_item, quantity, size = "medium"):
        self.menu_item = menu_item
        self.quantity = quantity
        self.size = size
        self.line_total = 0.0

    def calculate_line_total(self):
       self.line_total = self.menu_item.get_price(self.size) * self.quantity

    def __str__(self):
        if self.menu_item.sizes is None:
            return str(self.quantity) + " x " + self.menu_item.name + " - $" + str(self.line_total)
        else:
            return str(self.quantity) + " x " + self.menu_item.name + " (" + self.size + ") - $" + str(self.line_total)

"""Represents the entire order (multiple OrderItem objects)."""
class Order:
    def __init__(self):
        self.items = []          # list of OrderItem
        self.coupon_type = None  # 'percent' or 'fixed' or None
        self.coupon_amount = 0.0
        self.tip_percent = 0.0
        self.delivery = False

    def add_item(self, menu_item, quantity, size):
        item = OrderItem(menu_item, quantity, size)
        item.calculate_line_total()
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.menu_item.name == item_name:
                self.items.remove(item)
                print("Item removed!")

    def update_quantity(self, item_name, new_quantity):
        for item in self.items:
            if item.menu_item.name == item_name:
                item.quantity = new_quantity
                item.calculate_line_total()
                print("Quantity updated!")

    def view_order(self):
        print("\n-------- Current Order --------")

        num = 1
        for item in self.items:
            print(str(num) + ".) " + str(item))
            num += 1

        print("\nSubtotal: $" + str(self.calculate_subtotal()))
        print("---------------------------------")

    def calculate_subtotal(self):
        total = 0
        for item in self.items:
           total += item.line_total

        return total

    def apply_coupon(self):
        subtotal = self.calculate_subtotal()

        if  self.coupon_type == "percentage":
            discount = subtotal * (self.coupon_amount/100)
            return subtotal - discount
        elif self.coupon_type == "dollar":
            return subtotal - self.coupon_amount

        return subtotal

    def calculate_total_with_tax_and_tip(self):
        subtotal = self.apply_coupon()

        tax = subtotal * 0.06625
        tip = subtotal * self.tip_percent

        if self.delivery:
            deliveryFee = 5
        else:
            deliveryFee = 0

        return subtotal + tip + tax + deliveryFee

    def save_to_csv(self, filename):
        with open(filename, "w", newline = "") as outfile:
            write = csv.writer(outfile)

            write.writerow(["Item Name", "Quantity", "Price"])

            for row in self.items:
                write.writerow([row.menu_item.name, row.quantity, row.menu_item.get_price(row.size)])

        print("\nOrder saved to orderP5.csv!")

    def view_file(self, filename):
        print("\nCSV File:")

        with open(filename, "r") as infile:
            read = csv.reader(infile)

            for row in read:
                print(row)

"""Ties together restaurant info, menu, and a current order."""
class Restaurant:
    def __init__(self, name, location, url):
        self.name = name
        self.location = location
        self.url = url
        self.menu = Menu()
        self.current_order = Order()

    def display_info(self):
        print("\n-------- Restaurant Info --------")
        print("Welcome to " + self.name)
        print("Location: " + self.location)
        print("Website: " + self.url)
        print("---------------------------------")

    def order_from_category(self, category_name, allow_sizes = False):
        self.menu.show_category(category_name)

        ordering = input("\nWould you like to order (yes/no): ").lower()

        if ordering == "yes":

            order = int(input("Enter item number: " ))

            item = self.menu.get_item_by_number(category_name, order)

            qty = int(input("How many do you want? "))

            size = "medium"
            if allow_sizes:
                size = input("What size do you want? (small/medium/large): ").lower()

                if size not in item.sizes:
                    size = "medium"

            self.current_order.add_item(item, qty, size)

    def modify_order(self):
        self.current_order.view_order()

        modify = input("\nDo you want to modify order? (yes/no): ").lower()

        if modify == "yes":
            orderNum = int(input("Enter the item number to modify: "))
            orderNum = orderNum - 1

            if 0 <= orderNum and orderNum < len(self.current_order.items):
                action = input("Are you deleting or changing the quantity of the item? (delete/change): ").lower()

                item = self.current_order.items[orderNum]
                item_name = item.menu_item.name

                if action == "delete":
                    self.current_order.remove_item(item_name)
                elif action == "change":
                    newQty = int(input("Enter the new quantity of the item: "))
                    self.current_order.update_quantity(item_name, newQty)

    def place_order(self):
        print("\nPlacing order: ")

        subtotal = self.current_order.calculate_subtotal()

        print("\nSubtotal: $" + str(subtotal))

        coupon = input("\nDo you have a coupon? (yes or no): ").lower()

        if coupon == "yes":
            cType = input("Is the coupon percentage or dollar? ").lower()

            if cType == "percentage":
                amount = int(input("Enter percentage (wihtout %): "))
            elif cType == "dollar":
                amount = float(input("Enter dollar amount: $"))

            self.current_order.coupon_type = cType
            self.current_order.coupon_amount = amount

        discountedTotal = self.current_order.apply_coupon()
        print("\nSubtotal after coupon: $" + str(discountedTotal))

        print("\nTip options: 15%, 18%, 20%, 25%")

        tipChoice = int(input("Enter the tip (without %): "))
        self.current_order.tip_percent = tipChoice/100

        method = input("\nDo you want delivery (yes or no)? ").lower()

        if method == "yes":
            self.current_order.delivery = True
        else:
            self.current_order.delivery = False

        total = self.current_order.calculate_total_with_tax_and_tip()

        print("\nFinal total: $" + str(total))

        self.current_order.save_to_csv("orderP5.csv")

    def view_order_file(self):
        self.current_order.view_file("orderP5.csv")

def create_menu(restaurant):

    # Appetizers
    restaurant.menu.add_item(MenuItem("Takoyaki Octopus Balls (5pcs)", 8.99, "Appetizers"))
    restaurant.menu.add_item(MenuItem("Pan-Fried Gyoza Dumplings (6pcs)", 7.99, "Appetizers"))
    restaurant.menu.add_item(MenuItem("Shrimp Tempura (4pcs)", 7.99, "Appetizers"))
    restaurant.menu.add_item(MenuItem("Steamed Pork Bao Buns (2pcs)", 8.99, "Appetizers"))
    restaurant.menu.add_item(MenuItem("Yakitori Platter (5 Skewers)", 15.95, "Appetizers"))

    # Entrees
    restaurant.menu.add_item(MenuItem("Tonkatsu Omurice with Curry Sauce", 24.99, "Entrees"))
    restaurant.menu.add_item(MenuItem("Yinyang Bowl", 20.99, "Entrees"))
    restaurant.menu.add_item(MenuItem("Kyushu Spicy Tonkotsu Ramen", 17.99, "Entrees"))
    restaurant.menu.add_item(MenuItem("Diced Braised Pork Don", 14.99, "Entrees"))
    restaurant.menu.add_item(MenuItem("Katsuobushi Pork Ramen", 18.99, "Entrees"))

    # Desserts
    restaurant.menu.add_item(MenuItem("Matcha Tiramisu", 7.99, "Desserts"))
    restaurant.menu.add_item(MenuItem("Matcha Pudding with Red Bean", 4.99, "Desserts"))
    restaurant.menu.add_item(MenuItem("Japanese Cherry Blossom Jelly", 4.99, "Desserts"))
    restaurant.menu.add_item(MenuItem("Matcha Mille Crepe Cake", 9.99, "Desserts"))
    restaurant.menu.add_item(MenuItem("Mango Mille Crepe Cake", 9.99, "Desserts"))

    # Beverages
    sizes = {"small": -1, "medium": 0, "large": 1}

    restaurant.menu.add_item(MenuItem("Thai Iced Tea", 4.99, "Beverages", sizes))
    restaurant.menu.add_item(MenuItem("Amazing Lemonade", 4.99, "Beverages", sizes))
    restaurant.menu.add_item(MenuItem("Moshi Yuzu Sparkling Drink (Original)", 5.99, "Beverages", sizes))
    restaurant.menu.add_item(MenuItem("Moshi Yuzu Sparkling Drink (White Peach)", 5.99, "Beverages", sizes))
    restaurant.menu.add_item(MenuItem("Japanese Ramune", 4.25, "Beverages", sizes))

def main():
    restaurant = Restaurant("Kyuramen", "Old Bridge, NJ", "https://www.kyuramen.com/menu?menu=old-bridge-nj")

    create_menu(restaurant)
    open(fileName := "orderP5.csv", "w", newline = "").close()

    while True:
        print("\n=== OOP Restaurant Ordering System ===")
        print("1. View restaurant information")
        print("2. Order appetizers")
        print("3. Order entrees")
        print("4. Order desserts")
        print("5. Order beverages")
        print("6. View current order")
        print("7. Modify order")
        print("8. Place order")
        print("9. View order file")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            restaurant.display_info()
        elif choice == "2":
            restaurant.order_from_category("Appetizers")
        elif choice == "3":
            restaurant.order_from_category("Entrees")
        elif choice == "4":
            restaurant.order_from_category("Desserts")
        elif choice == "5":
            restaurant.order_from_category("Beverages", True)
        elif choice == "6":
            restaurant.current_order.view_order()
        elif choice == "7":
            restaurant.modify_order()
        elif choice == "8":
            restaurant.place_order()
        elif choice == "9":
            restaurant.view_order_file()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
