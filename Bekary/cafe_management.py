import pandas as pd
from datetime import datetime

class BakeryOrderManagement:
    def __init__(self):
        self.load_orders()

    def load_orders(self):
        try:
            self.orders = pd.read_excel("bakery_orders.xlsx")
        except FileNotFoundError:
            self.orders = pd.DataFrame(columns=["Customer Name", "Item", "Quantity", "Order Date"])

    def save_orders(self):
        self.orders.to_excel("bakery_orders.xlsx", index=False)

    def add_order(self):
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
        new_order = pd.DataFrame([[customer_name, item, quantity, order_date]],
                                 columns=["Customer Name", "Item", "Quantity", "Order Date"])
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
        if order_id < 0 or order_id >= len(self.orders):
            print("Invalid order ID. Order not found.")
        else:
            print("Updating Order ID:", order_id)
            self.orders.at[order_id, "Item"] = input("Enter new item: ")
            while True:
                try:
                    self.orders.at[order_id, "Quantity"] = int(input("Enter new quantity: "))
                    if self.orders.at[order_id, "Quantity"] > 0:
                        break
                    else:
                        print("Quantity must be a positive integer. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")
            print("Order updated successfully!")


# Using the system
order_system = BakeryOrderManagement()

while True:
    print("\n1. Add Order\n2. View Orders\n3. Update Order\n4. Save to Excel\n5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        order_system.add_order()
    elif choice == '2':
        order_system.view_orders()
    elif choice == '3':
        order_system.update_order()
    elif choice == '4':
        order_system.save_orders()
        print("Orders saved to 'bakery_orders.xlsx'.")
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")
