import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from datetime import datetime

class ShoppingCenterSystem:
    def __init__(self, master):
        self.master = master
        master.title("Shopping Center System")

        # Create labels and entry widgets
        self.label_customer_name = ttk.Label(master, text="Customer Name:")
        self.entry_customer_name = ttk.Entry(master)

        self.label_item_name = ttk.Label(master, text="Item Name:")
        self.entry_item_name = ttk.Entry(master)

        self.label_item_price = ttk.Label(master, text="Item Price:")
        self.entry_item_price = ttk.Entry(master)

        # Create buttons
        self.button_record = ttk.Button(master, text="Record Purchase", command=self.record_purchase)
        self.button_print_slip = ttk.Button(master, text="Print Slip", command=self.print_slip)
        self.button_export_excel = ttk.Button(master, text="Export to Excel", command=self.export_to_excel)
        self.button_update_record = ttk.Button(master, text="Update Record", command=self.update_record)
        self.button_view_record = ttk.Button(master, text="View Record", command=self.view_record)

        # Layout using grid
        self.label_customer_name.grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.entry_customer_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_item_name.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_item_name.grid(row=1, column=1, padx=10, pady=5)

        self.label_item_price.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.entry_item_price.grid(row=2, column=1, padx=10, pady=5)

        self.button_record.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_print_slip.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_export_excel.grid(row=5, column=0, columnspan=2, pady=10)
        self.button_update_record.grid(row=6, column=0, columnspan=2, pady=10)
        self.button_view_record.grid(row=7, column=0, columnspan=2, pady=10)

        # Data storage
        self.purchase_data = []

    def record_purchase(self):
        customer_name = self.entry_customer_name.get()
        item_name = self.entry_item_name.get()
        item_price = self.entry_item_price.get()

        if customer_name and item_name and item_price:
            customer_id = self.generate_customer_id()
            discounted_price = self.calculate_discount(float(item_price))
            purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.purchase_data.append({
                "Customer ID": customer_id,
                "Customer Name": customer_name,
                "Item Name": item_name,
                "Item Price": item_price,
                "Discounted Price": discounted_price,
                "Purchase Date": purchase_date
            })

            messagebox.showinfo("Recorded", "Purchase recorded successfully.\nCustomer ID: " + str(customer_id))
            self.clear_entries()
        else:
            messagebox.showwarning("Incomplete Information", "Please enter all required information.")

    def print_slip(self):
        if self.purchase_data:
            pdf_filename = "purchase_slip.pdf"
            c = canvas.Canvas(pdf_filename)

            c.drawString(100, 750, "Shopping Center Purchase Slip")
            c.drawString(100, 730, "-" * 40)

            y_position = 710
            for purchase_record in self.purchase_data:
                c.drawString(100, y_position, f"Customer ID: {purchase_record['Customer ID']}")
                y_position -= 20
                c.drawString(100, y_position, f"Customer Name: {purchase_record['Customer Name']}")
                y_position -= 20
                c.drawString(100, y_position, f"Item Name: {purchase_record['Item Name']}")
                y_position -= 20
                c.drawString(100, y_position, f"Item Price: ${purchase_record['Item Price']}")
                y_position -= 20
                c.drawString(100, y_position, f"Discounted Price: ${purchase_record['Discounted Price']}")
                y_position -= 20
                c.drawString(100, y_position, f"Purchase Date: {purchase_record['Purchase Date']}")
                y_position -= 40

            c.save()
            messagebox.showinfo("Printed Slip", f"Purchase slip printed to {pdf_filename}.")
        else:
            messagebox.showwarning("No Data", "No purchase data available to print.")

    def export_to_excel(self):
        if self.purchase_data:
            excel_filename = "purchase_data.xlsx"
            wb = Workbook()
            ws = wb.active

            headers = ["Customer ID", "Customer Name", "Item Name", "Item Price", "Discounted Price", "Purchase Date"]
            ws.append(headers)

            for purchase_record in self.purchase_data:
                ws.append([purchase_record[header] for header in headers])

            wb.save(excel_filename)
            messagebox.showinfo("Exported to Excel", f"Data exported to {excel_filename}.")
        else:
            messagebox.showwarning("No Data", "No purchase data available to export.")

    def update_record(self):
        if self.purchase_data:
            customer_id = simpledialog.askstring("Update Record", "Enter Customer ID to update record:")
            if customer_id:
                for purchase_record in self.purchase_data:
                    if purchase_record["Customer ID"] == customer_id:
                        new_item_price = simpledialog.askfloat("Update Record", "Enter new Item Price:")
                        if new_item_price is not None:
                            purchase_record["Item Price"] = new_item_price
                            purchase_record["Discounted Price"] = self.calculate_discount(new_item_price)
                            messagebox.showinfo("Updated Record", "Record updated successfully.")
                            return
                messagebox.showwarning("Customer ID not found", "No record found with the given Customer ID.")
        else:
            messagebox.showwarning("No Data", "No purchase data available to update.")

    def view_record(self):
        if self.purchase_data:
            record_text = "Purchase Records:\n\n"
            for purchase_record in self.purchase_data:
                record_text += f"Customer ID: {purchase_record['Customer ID']}\n"
                record_text += f"Customer Name: {purchase_record['Customer Name']}\n"
                record_text += f"Item Name: {purchase_record['Item Name']}\n"
                record_text += f"Item Price: ${purchase_record['Item Price']}\n"
                record_text += f"Discounted Price: ${purchase_record['Discounted Price']}\n"
                record_text += f"Purchase Date: {purchase_record['Purchase Date']}\n\n"

            messagebox.showinfo("Purchase Records", record_text)
        else:
            messagebox.showwarning("No Data", "No purchase data available to view.")

    def calculate_discount(self, item_price):
        # Add your discount calculation logic here (if needed)
        # For example, let's say we apply a 10% discount
        discount_percentage = 10
        discounted_price = item_price - (item_price * (discount_percentage / 100))
        return round(discounted_price, 2)

    def generate_customer_id(self):
        # Generate a unique customer ID based on the current timestamp
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        return int(timestamp_str)

    def clear_entries(self):
        self.entry_customer_name.delete(0, tk.END)
        self.entry_item_name.delete(0, tk.END)
        self.entry_item_price.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCenterSystem(root)
    root.mainloop()
