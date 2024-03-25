import pandas as pd
from datetime import datetime

class BakerySystem:
    def __init__(self):
        self.load_data()

    def load_data(self):
        try:
            self.orders = pd.read_excel("bakery_orders.xlsx")
        except FileNotFoundError:
            self.orders = pd.DataFrame(columns=["Order_ID", "Customer_Name", "Item", "Quantity", "Order_Date"])

    def save_data(self):
        self.orders.to_excel("bakery_orders.xlsx", index=False)
        print("Data saved successfully.")

    def add_order(self):
        order_id = len(self.orders) + 1
        customer_name = input("Enter customer name: ")
        item = input("Enter item ordered: ")
        while True:
            try:
                quantity = int(input("Enter quantity: "))
                if quantity > 0:
                    break
                else:
                    print("Quantity must be a positive integer. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_order = pd.DataFrame([[order_id, customer_name, item, quantity, order_date]],
                                 columns=["Order_ID", "Customer_Name", "Item", "Quantity", "Order_Date"])
        self.orders = pd.concat([self.orders, new_order], ignore_index=True)
        print("Order added successfully!")

    def view_orders(self):
        if self.orders.empty:
            print("No orders available.")
        else:
            print(self.orders)

    def update_order(self):
        if self.orders.empty:
            print("No orders available for updating.")
            return

        order_id = int(input("Enter order ID to update: "))
        if order_id < 1 or order_id > len(self.orders):
            print("Invalid order ID. Order not found.")
        else:
            print("Updating Order ID:", order_id)
            self.orders.at[order_id - 1, "Item"] = input("Enter new item: ")
            while True:
                try:
                    self.orders.at[order_id - 1, "Quantity"] = int(input("Enter new quantity: "))
                    if self.orders.at[order_id - 1, "Quantity"] > 0:
                        break
                    else:
                        print("Quantity must be a positive integer. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")
            print("Order updated successfully!")

# Using the bakery system
bakery_system = BakerySystem()

while True:
    print("\n1. Add Order\n2. View Orders\n3. Update Order\n4. Save Data\n5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        bakery_system.add_order()
    elif choice == '2':
        bakery_system.view_orders()
    elif choice == '3':
        bakery_system.update_order()
    elif choice == '4':
        bakery_system.save_data()
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")
