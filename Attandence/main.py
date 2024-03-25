import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class BakerySystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bakery Management System")

        # Initialize the bakery system
        self.bakery_system = BakerySystem()

        # Create widgets
        self.label = tk.Label(master, text="Bakery Management System")
        self.label.pack()

        self.button_add_order = tk.Button(master, text="Add Order", command=self.add_order)
        self.button_add_order.pack()

        self.button_view_orders = tk.Button(master, text="View Orders", command=self.view_orders)
        self.button_view_orders.pack()

        self.button_update_order = tk.Button(master, text="Update Order", command=self.update_order)
        self.button_update_order.pack()

        self.button_save_data = tk.Button(master, text="Save Data", command=self.save_data)
        self.button_save_data.pack()

        self.button_exit = tk.Button(master, text="Exit", command=self.exit_program)
        self.button_exit.pack()

    def add_order(self):
        AddOrderWindow(self.master, self.bakery_system)

    def view_orders(self):
        ViewOrdersWindow(self.master, self.bakery_system)

    def update_order(self):
        UpdateOrderWindow(self.master, self.bakery_system)

    def save_data(self):
        self.bakery_system.save_data()
        messagebox.showinfo("Information", "Data saved successfully.")

    def exit_program(self):
        self.master.destroy()

class AddOrderWindow:
    def __init__(self, master, bakery_system):
        self.master = tk.Toplevel(master)
        self.master.title("Add Order")

        self.bakery_system = bakery_system

        # Create widgets
        self.label_customer_name = tk.Label(self.master, text="Customer Name:")
        self.entry_customer_name = tk.Entry(self.master)

        self.label_item = tk.Label(self.master, text="Item:")
        self.entry_item = tk.Entry(self.master)

        self.label_quantity = tk.Label(self.master, text="Quantity:")
        self.entry_quantity = tk.Entry(self.master)

        self.button_submit = tk.Button(self.master, text="Submit", command=self.submit_order)

        # Grid layout
        self.label_customer_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_customer_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_item.grid(row=1, column=0, padx=10, pady=10)
        self.entry_item.grid(row=1, column=1, padx=10, pady=10)

        self.label_quantity.grid(row=2, column=0, padx=10, pady=10)
        self.entry_quantity.grid(row=2, column=1, padx=10, pady=10)

        self.button_submit.grid(row=3, column=0, columnspan=2, pady=10)

    def submit_order(self):
        customer_name = self.entry_customer_name.get()
        item = self.entry_item.get()
        try:
            quantity = int(self.entry_quantity.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid integer.")
            return

        self.bakery_system.add_order(customer_name, item, quantity)
        messagebox.showinfo("Information", "Order added successfully.")
        self.master.destroy()

class ViewOrdersWindow:
    def __init__(self, master, bakery_system):
        self.master = tk.Toplevel(master)
        self.master.title("View Orders")

        self.bakery_system = bakery_system

        # Create widgets
        self.text_widget = tk.Text(self.master, wrap="none")
        self.text_widget.insert("1.0", self.bakery_system.view_orders())
        self.text_widget.config(state="disabled")
        self.text_widget.pack(fill="both", expand=True)

class UpdateOrderWindow:
    def __init__(self, master, bakery_system):
        self.master = tk.Toplevel(master)
        self.master.title("Update Order")

        self.bakery_system = bakery_system

        # Create widgets
        self.label_order_id = tk.Label(self.master, text="Order ID:")
        self.entry_order_id = tk.Entry(self.master)

        self.label_new_item = tk.Label(self.master, text="New Item:")
        self.entry_new_item = tk.Entry(self.master)

        self.label_new_quantity = tk.Label(self.master, text="New Quantity:")
        self.entry_new_quantity = tk.Entry(self.master)

        self.button_update = tk.Button(self.master, text="Update", command=self.update_order)

        # Grid layout
        self.label_order_id.grid(row=0, column=0, padx=10, pady=10)
        self.entry_order_id.grid(row=0, column=1, padx=10, pady=10)

        self.label_new_item.grid(row=1, column=0, padx=10, pady=10)
        self.entry_new_item.grid(row=1, column=1, padx=10, pady=10)

        self.label_new_quantity.grid(row=2, column=0, padx=10, pady=10)
        self.entry_new_quantity.grid(row=2, column=1, padx=10, pady=10)

        self.button_update.grid(row=3, column=0, columnspan=2, pady=10)

    def update_order(self):
        try:
            order_id = int(self.entry_order_id.get())
            if order_id <= 0 or order_id > len(self.bakery_system.orders):
                messagebox.showerror("Error", "Invalid order ID. Order not found.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid order ID. Please enter a valid integer.")
            return

        new_item = self.entry_new_item.get()
        try:
            new_quantity = int(self.entry_new_quantity.get())
            if new_quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid integer.")
            return

        self.bakery_system.update_order(order_id, new_item, new_quantity)
        messagebox.showinfo("Information", "Order updated successfully.")
        self.master.destroy()

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

    def add_order(self, customer_name, item, quantity):
        order_id = len(self.orders) + 1
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_order = pd.DataFrame([[order_id, customer_name, item, quantity, order_date]],
                                 columns=["Order_ID", "Customer_Name", "Item", "Quantity", "Order_Date"])
        self.orders = pd.concat([self.orders, new_order], ignore_index=True)

    def view_orders(self):
        if self.orders.empty:
            return "No orders available."
        else:
            return self.orders.to_string(index=False)

    def update_order(self, order_id, new_item, new_quantity):
        self.orders.at[order_id - 1, "Item"] = new_item
        self.orders.at[order_id - 1, "Quantity"] = new_quantity

if __name__ == "__main__":
    root = tk.Tk()
    app = BakerySystemGUI(root)
    root.mainloop()

