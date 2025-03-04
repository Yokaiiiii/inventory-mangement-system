import time
import tkinter as tk
from tkinter import messagebox
import os

from employee import connect_database
from products_page import create_tree_view

COLORS = {
    "background": "#181C14",  # Dark background
    "frame": "#3C3D37",  # Sidebar and frames
    "highlight": "#697565",  # Subtitles, highlights
    "text": "#ECDFCC"  # Light text color for contrast
}


def generate_unique_key():
    # Get the current timestamp (in seconds)
    timestamp = int(time.time())

    # Use modular arithmetic to get a 4-digit number
    return str(timestamp % 10000)  # This will ensure the result is always a 4-digit number


# Example usage
user_key = generate_unique_key()
print(user_key)


def product_treeview_data():
    connection, cursor = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("""
        SELECT productid, name, quantity, price, status FROM product_data WHERE status = 'Active' AND quantity > 0 ORDER BY productid
        """)
        product_records = cursor.fetchall()
        billing_product_tree_view.delete(*billing_product_tree_view.get_children())

        for record in product_records:
            billing_product_tree_view.insert('', 'end', values=record)
    except Exception as error:
        messagebox.showerror("Error", str(error))

    finally:
        cursor.close()
        connection.close()


def search_product_by_name(product_name):
    if product_name == '':
        messagebox.showerror("Error", "Please enter a product name")
    else:
        connection, cursor = connect_database()
        if not connection or not cursor:
            return
        try:
            cursor.execute("""
            SELECT productid, name, quantity, price, status FROM product_data WHERE name LIKE %s
            """, f"%{product_name}%")
            records = cursor.fetchall()
            billing_product_tree_view.delete(*billing_product_tree_view.get_children())
            for record in records:
                billing_product_tree_view.insert('', 'end', values=record)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            connection.close()
            cursor.close()


def show_all_products(product_name_entry):
    product_treeview_data()
    product_name_entry.delete(0, 'end')


generated_bill = {}


def clear_product_from_bill(product_name_entry, quantity_entry):
    generated_bill.clear()
    billing_tree_view.delete(*billing_tree_view.get_children())
    product_name_entry.delete(0, "end")
    quantity_entry.delete(0, "end")


def add_product_to_bill(product_id_entry, quantity_entry, total_product_label, total_price_label):
    product_id = product_id_entry.get()
    quantity = int(quantity_entry.get())
    if product_id == '' or quantity == '':
        messagebox.showerror("Error", "Please enter all fields")
    else:
        connection, cursor = connect_database()
        if not connection or not cursor:
            return
        try:
            cursor.execute("SELECT productid, quantity, status, name, price FROM product_data WHERE productid = %s",
                           product_id)
            records = cursor.fetchone()
            name = records[3]
            price = int(records[4])
            if records[2] == "Active" and int(records[1]) >= quantity:
                if product_id in generated_bill.keys():
                    generated_bill[product_id][2] = quantity
                    generated_bill[product_id][3] = price * quantity
                else:
                    data = [name, price, quantity, price * quantity]
                    generated_bill[product_id] = data

                if generated_bill[product_id][2] <= 0:
                    generated_bill.pop(product_id)

                # print(generated_bill)
                billing_tree_view.delete(*billing_tree_view.get_children())
                for record in generated_bill.values():
                    billing_tree_view.insert("", "end", values=record)

                total_product = len(generated_bill.keys())
                total_price = 0
                for val in generated_bill.values():
                    total_price += val[3]

                total_product_label.configure(text=f"Total Product:\t\t {total_product}")
                total_price_label.configure(text=f"Total Price:\t\t Rs {total_price}")
            else:
                print("Fuck you, you cannot buy it")

        except Exception as error:
            messagebox.showerror("Error", str(error))
        finally:
            product_id_entry.delete(0, 'end')
            quantity_entry.delete(0, 'end')
            cursor.close()
            connection.close()


def create_billing_table():
    connection, cursor = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_data (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            customer_contact VARCHAR(15) NOT NULL UNIQUE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        connection.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing_data (
            bill_id VARCHAR(10) PRIMARY KEY,
            customer_id INT NOT NULL,
            bill_date DATE NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            discount DECIMAL(5, 2) DEFAULT 0,
            net_amount DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id) ON UPDATE CASCADE
            );
        """)

        connection.commit()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bill_id VARCHAR(10) NOT NULL,
            productid INT NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL,
            net_price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES billing_data(bill_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (productid) REFERENCES product_data(productid) ON UPDATE CASCADE
        );
        """)

        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        connection.close()


def generate_bill_original(customer_name_entry, customer_contact_entry, discount_entry):
    customer_name = customer_name_entry.get()
    customer_contact = customer_contact_entry.get()
    discount = discount_entry.get()
    discount = 0 if discount == '' else int(discount) / 100

    if customer_name == '' or customer_contact == '':
        messagebox.showerror("Error", "Please enter customer details")
        return

    if not generated_bill:
        messagebox.showerror("Error", "No products added to bill")
        return

    try:
        # Generate a unique bill ID
        bill_id = generate_unique_key()

        # Calculate total amount
        total_amount = 0
        for product in generated_bill.values():
            total_amount += product[3]  # sum of net prices

        # Apply discount
        discounted_amount = total_amount * (1 - discount)

        # Connect to database
        connection, cursor = connect_database()
        if not connection or not cursor:
            return

        # Start a transaction
        connection.begin()

        try:
            # First check if customer exists or create new customer record
            cursor.execute("""
                SELECT customer_id FROM customer_data WHERE customer_contact = %s
            """, (customer_contact,))

            customer_result = cursor.fetchone()

            if customer_result:
                customer_id = customer_result[0]
                # Update customer name in case it changed
                cursor.execute("""
                    UPDATE customer_data SET customer_name = %s WHERE customer_id = %s
                """, (customer_name, customer_id))
            else:
                # Insert new customer
                cursor.execute("""
                    INSERT INTO customer_data (customer_name, customer_contact)
                    VALUES (%s, %s)
                """, (customer_name, customer_contact))
                customer_id = cursor.lastrowid

            # Insert into billing_data table
            cursor.execute("""
                INSERT INTO billing_data 
                (bill_id, customer_id, bill_date, total_amount, discount, net_amount) 
                VALUES (%s, %s, CURRENT_DATE(), %s, %s, %s)
            """, (bill_id, customer_id, total_amount, discount * 100, discounted_amount))

            # Insert product details into billing_details table and update product quantities
            for product_id, product_info in generated_bill.items():
                product_name = product_info[0]
                price = product_info[1]
                quantity = product_info[2]
                net_price = product_info[3]

                # Insert into billing_details
                cursor.execute("""
                    INSERT INTO billing_details 
                    (bill_id, productid, product_name, price, quantity, net_price) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (bill_id, product_id, product_name, price, quantity, net_price))

                # Update product quantity in product_data
                cursor.execute("""
                    UPDATE product_data 
                    SET quantity = quantity - %s 
                    WHERE productid = %s
                """, (quantity, product_id))

            # Commit the transaction
            connection.commit()

            # Show success message
            messagebox.showinfo("Success", f"Bill generated successfully!\nBill ID: {bill_id}")

            # Clear the bill after successful generation
            generated_bill.clear()
            billing_tree_view.delete(*billing_tree_view.get_children())
            customer_name_entry.delete(0, "end")
            customer_contact_entry.delete(0, "end")
            discount_entry.delete(0, "end")

        except Exception as e:
            # Rollback in case of error
            connection.rollback()
            messagebox.showerror("Database Error", f"Failed to generate bill: {str(e)}")

    except Exception as error:
        messagebox.showerror("Error", str(error))

    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()


def generate_bill(customer_name_entry, customer_contact_entry, discount_entry):
    customer_name = customer_name_entry.get()
    customer_contact = customer_contact_entry.get()
    discount = discount_entry.get()
    discount = 0 if discount == '' else int(discount) / 100

    if customer_name == '' or customer_contact == '':
        messagebox.showerror("Error", "Please enter customer details")
        return

    if not generated_bill:
        messagebox.showerror("Error", "No products added to bill")
        return

    try:
        # Generate a unique bill ID
        bill_id = generate_unique_key()

        # Calculate total amount
        total_amount = 0
        for product in generated_bill.values():
            total_amount += product[3]  # sum of net prices

        # Apply discount
        discount_amount = total_amount * discount
        discounted_amount = total_amount - discount_amount

        # Connect to database
        connection, cursor = connect_database()
        if not connection or not cursor:
            return

        # Start a transaction
        connection.begin()

        try:
            # First check if customer exists or create new customer record
            cursor.execute("""
                SELECT customer_id FROM customer_data WHERE customer_contact = %s
            """, (customer_contact,))

            customer_result = cursor.fetchone()

            if customer_result:
                customer_id = customer_result[0]
                # Update customer name in case it changed
                cursor.execute("""
                    UPDATE customer_data SET customer_name = %s WHERE customer_id = %s
                """, (customer_name, customer_id))
            else:
                # Insert new customer
                cursor.execute("""
                    INSERT INTO customer_data (customer_name, customer_contact)
                    VALUES (%s, %s)
                """, (customer_name, customer_contact))
                customer_id = cursor.lastrowid

            # Insert into billing_data table
            cursor.execute("""
                INSERT INTO billing_data 
                (bill_id, customer_id, bill_date, total_amount, discount, net_amount) 
                VALUES (%s, %s, CURRENT_DATE(), %s, %s, %s)
            """, (bill_id, customer_id, total_amount, discount * 100, discounted_amount))

            # Insert product details into billing_details table and update product quantities
            for product_id, product_info in generated_bill.items():
                product_name = product_info[0]
                price = product_info[1]
                quantity = product_info[2]
                net_price = product_info[3]

                # Insert into billing_details
                cursor.execute("""
                    INSERT INTO billing_details 
                    (bill_id, productid, product_name, price, quantity, net_price) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (bill_id, product_id, product_name, price, quantity, net_price))

                # Update product quantity in product_data
                cursor.execute("""
                    UPDATE product_data 
                    SET quantity = quantity - %s 
                    WHERE productid = %s
                """, (quantity, product_id))

            # Commit the transaction
            connection.commit()

            # Generate bill details for display
            current_date = time.strftime("%Y-%m-%d")
            current_time = time.strftime("%H:%M:%S")

            # Create a detailed bill for display
            bill_details = f"""
{"=" * 50}
             STORE BILLING SYSTEM
{"=" * 50}
Bill ID: {bill_id}
Date: {current_date}
Time: {current_time}
{"-" * 50}
Customer Name: {customer_name}
Contact: {customer_contact}
{"-" * 50}
                ITEMS
{"-" * 50}
{"Item Name":<25}{"Price":>8} {"Qty":>5} {"Total":>10}
{"-" * 50}
"""

            for product_id, product_info in generated_bill.items():
                product_name = product_info[0]
                price = product_info[1]
                quantity = product_info[2]
                net_price = product_info[3]

                # Truncate product name if too long
                display_name = product_name[:22] + "..." if len(product_name) > 25 else product_name
                bill_details += f"{display_name:<25}{price:>8} {quantity:>5} {net_price:>10}\n"

            bill_details += f"""{"-" * 50}
"""
            bill_details += f"{"Subtotal:":<25}{total_amount:>23}\n"
            bill_details += f"{"Discount (" + str(int(discount * 100)) + "%):":<25}{discount_amount:>23}\n"
            bill_details += f"{"Grand Total:":<25}{discounted_amount:>23}\n"
            bill_details += f"""{"=" * 50}
          Thank You For Shopping!
{"=" * 50}
"""

            # Show detailed bill
            receipt_window = tk.Toplevel()
            receipt_window.title(f"Bill Receipt - {bill_id}")
            receipt_window.geometry("500x600")
            receipt_window.resizable(False, False)
            receipt_window.configure(bg=COLORS["background"])

            # Add a scrollable text area for the bill
            bill_frame = tk.Frame(receipt_window, bg=COLORS["background"])
            bill_frame.pack(fill="both", expand=True, padx=10, pady=10)

            bill_text = tk.Text(bill_frame, bg="white", fg="black", font=("Courier", 10))
            bill_text.pack(fill="both", expand=True)
            bill_text.insert(tk.END, bill_details)
            bill_text.config(state="disabled")  # Make read-only

            # Add print and close buttons
            button_frame = tk.Frame(receipt_window, bg=COLORS["background"])
            button_frame.pack(fill="x", pady=10)

            def print_bill():
                # In a real application, you would implement printer functionality
                # For now, we'll just show a message
                messagebox.showinfo("Print", "Sending bill to printer...")

            def save_bill():
                # Save bill to a text file
                try:
                    file_path = f"bills/bill_{bill_id}.txt"
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if it doesn't exist
                    with open(file_path, "w") as file:
                        file.write(bill_details)
                    messagebox.showinfo("Save", f"Bill saved to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save bill: {str(e)}")

            print_button = tk.Button(button_frame, text="Print", command=print_bill,
                                     font=("Times New Roman", 12), bg=COLORS["frame"], fg=COLORS["text"])
            print_button.pack(side="left", padx=10)

            save_button = tk.Button(button_frame, text="Save", command=save_bill,
                                    font=("Times New Roman", 12), bg=COLORS["frame"], fg=COLORS["text"])
            save_button.pack(side="left", padx=10)

            close_button = tk.Button(button_frame, text="Close", command=receipt_window.destroy,
                                     font=("Times New Roman", 12), bg=COLORS["frame"], fg=COLORS["text"])
            close_button.pack(side="right", padx=10)

            # Clear the bill after successful generation
            generated_bill.clear()
            billing_tree_view.delete(*billing_tree_view.get_children())
            customer_name_entry.delete(0, "end")
            customer_contact_entry.delete(0, "end")
            discount_entry.delete(0, "end")

        except Exception as e:
            # Rollback in case of error
            connection.rollback()
            messagebox.showerror("Database Error", f"Failed to generate bill: {str(e)}")

    except Exception as error:
        messagebox.showerror("Error", str(error))

    finally:
        cursor.close()
        connection.close()


def select_from_product(event, product_id_entry):
    index = billing_product_tree_view.selection()
    if not index:
        messagebox.showerror("Error", "Please select a product")
        return
    content = billing_product_tree_view.item(index[0])
    content = content["values"]

    product_id_entry.delete(0, "end")

    product_id_entry.insert(0, content[0])


def billing_form(window):
    global back_button_icon, billing_product_tree_view, billing_tree_view  # if we do not make this global, we do not get the back icon in the header
    # Create billing management frame
    billing_frame = tk.Frame(window, width=1270, height=588, bg=COLORS["background"])
    billing_frame.place(x=0, y=80)

    # giving the top heading for the page
    billing_heading_label = tk.Label(
        billing_frame,
        text="Manage Billing Details",
        font=("Times New Roman", 16, "bold"),
        bg=COLORS["text"],  # Light background for visibility
        fg=COLORS["background"],  # Dark text for contrast
    )
    billing_heading_label.place(x=0, y=0, relwidth=1)

    # Back button to close the frame
    back_button_icon = tk.PhotoImage(file="./images/back.png")
    back_button = tk.Button(
        billing_frame, image=back_button_icon, bd=0, cursor="hand2",
        bg=COLORS["text"], command=lambda: billing_frame.place_forget()
    )
    back_button.place(x=5, y=0)

    left_frame = tk.Frame(billing_frame, width=378, height=550, bg=COLORS["background"])
    left_frame.place(x=5, y=35)
    left_frame.propagate(False)  # Prevents resizing beyond defined width/height

    left_heading_label = tk.Label(left_frame, text="All Products", font=("Times New Roman", 20, "bold"),
                                  bg=COLORS["highlight"], fg=COLORS["background"])
    left_heading_label.pack(fill="x", pady=(0, 10))

    left_searching_frame = tk.LabelFrame(left_frame, bg=COLORS["background"], text="Search Products by Name",
                                         fg=COLORS["text"])
    left_searching_frame.pack(fill='x')

    search_entry = tk.Entry(left_searching_frame, width=18, font=("Times New Roman", 12), bg="lightyellow", fg="black")

    search_entry.grid(row=0, column=0, padx=5, pady=13)

    search_button = tk.Button(left_searching_frame, text="Search", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=7,
                              command=lambda: search_product_by_name(search_entry.get())
                              )

    search_button.grid(row=0, column=1, padx=5, pady=(0, 3))

    # Show all button
    show_all_button = tk.Button(left_searching_frame, text="Show All", font=("Times New Roman", 14, "bold"),
                                cursor="hand2",
                                fg=COLORS["text"], bg=COLORS["background"], width=7,
                                command=lambda: show_all_products(search_entry)
                                )

    show_all_button.grid(row=0, column=2, padx=5, pady=(0, 3))

    product_tree_view_columns = {
        "productid": ("Product ID", 80),
        "name": ("Name", 100),
        "quantity": ("Quantity", 80),
        "price": ("Price", 80),
        "status": ("Status", 100),
    }

    billing_product_tree_view = create_tree_view(370, 370, left_frame, product_tree_view_columns, 5, 150)
    product_treeview_data()

    remove_label = tk.Label(left_frame, text="Note: Enter 0 Quantity to remove product from the Cart",
                            font=("Times New Roman", 12, 'italic'), bg=COLORS["background"],
                            fg="red")
    remove_label.place(y=525, x=5)

    middle_frame = tk.Frame(billing_frame, width=500, height=550, bg=COLORS["background"])
    middle_frame.place(x=388, y=35)
    middle_frame.propagate(False)  # Prevents resizing beyond defined width/height

    customer_detail_frame = tk.Frame(middle_frame, bg=COLORS["background"])
    customer_detail_frame.pack(fill='x')
    customer_detail_label = tk.Label(
        customer_detail_frame,
        text="Customer Details",
        font=("Times New Roman", 20, "bold"),
        bg=COLORS["text"],  # Light background for visibility
        fg=COLORS["background"],  # Dark text for contrast
    )
    customer_detail_label.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=(0, 5))

    # Adjust column weights to ensure proper stretching
    customer_detail_frame.columnconfigure(1, weight=1)  # Entry fields stretch properly
    customer_detail_frame.columnconfigure(3, weight=1)  # Balance the right side

    # Name Label & Entry (Row 1)
    customer_name_label = tk.Label(
        customer_detail_frame, text="Name", font=("Times New Roman", 16, "bold"),
        bg=COLORS["background"], fg=COLORS["text"]
    )
    customer_name_label.grid(row=1, column=0, padx=(5, 2), pady=5, sticky="w")

    customer_name_entry = tk.Entry(
        customer_detail_frame, font=("Times New Roman", 14), width=18,
        bg="lightyellow", fg="black"
    )
    customer_name_entry.grid(row=1, column=1, padx=(2, 5), pady=5, sticky="ew")

    # Contact Label & Entry (Row 1 - Same as Name)
    contact_number_label = tk.Label(
        customer_detail_frame, text="Contact", font=("Times New Roman", 16, "bold"),
        bg=COLORS["background"], fg=COLORS["text"]
    )
    contact_number_label.grid(row=1, column=2, padx=(5, 2), pady=5, sticky="w")

    contact_number_entry = tk.Entry(
        customer_detail_frame, font=("Times New Roman", 14), width=18,
        bg="lightyellow", fg="black"
    )
    contact_number_entry.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="ew")

    cart_frame = tk.LabelFrame(middle_frame, bg=COLORS["background"], text="Cart", fg=COLORS["text"], height=330,
                               width=480)
    cart_frame.pack(padx=10, pady=5)

    billing_tree_view_columns = {
        "name": ("Name", 100),
        'price': ("Price", 100),
        "quantity": ("Quantity", 80),
        "net_price": ("Net Price", 80),
    }

    billing_tree_view = create_tree_view(295, 465, cart_frame, billing_tree_view_columns, 5, 5)

    add_product_frame = tk.Frame(middle_frame, bg=COLORS["background"])
    add_product_frame.pack(fill='x')

    product_id_label = tk.Label(add_product_frame, text="Product Id", font=("Times New Roman", 16, "bold"),
                                bg=COLORS["background"], fg=COLORS["text"])
    product_id_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

    product_id_entry = tk.Entry(add_product_frame, width=18, font=("Times New Roman", 12),
                                bg="lightyellow", fg="black")
    product_id_entry.grid(row=1, column=0, padx=5, pady=(5, 0))

    quantity_label = tk.Label(add_product_frame, text="Quantity", font=("Times New Roman", 16, "bold"),
                              bg=COLORS["background"], fg=COLORS["text"])
    quantity_label.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="w")

    quantity_entry = tk.Entry(add_product_frame, width=18, font=("Times New Roman", 12),
                              bg="lightyellow", fg="black")
    quantity_entry.grid(row=1, column=1, padx=5, pady=(5, 0))

    clear_button = tk.Button(add_product_frame, text="Clear", font=("Times New Roman", 14, "bold"), cursor="hand2",
                             fg=COLORS["text"], bg=COLORS["background"], width=12,
                             command=lambda: clear_product_from_bill(product_id_entry, quantity_entry))
    clear_button.grid(row=2, column=2, padx=10)

    add_button = tk.Button(add_product_frame, text="Add | Update", font=("Times New Roman", 14, "bold"), cursor="hand2",
                           fg=COLORS["text"], bg=COLORS["background"], width=12,
                           command=lambda: add_product_to_bill(product_id_entry, quantity_entry, total_product_label,
                                                               total_price_label))
    add_button.grid(row=1, column=2, padx=10, pady=10)

    right_frame = tk.Frame(billing_frame, width=370, height=550, bg=COLORS["background"])
    right_frame.place(x=893, y=35)
    right_frame.propagate(False)  # Prevents resizing beyond defined width/height

    right_frame_heading = tk.Label(
        right_frame,
        text="Customer Bill Area",
        font=("Times New Roman", 20, "bold"),
        bg=COLORS["highlight"],  # Light background for visibility
        fg='black',  # Dark text for contrast
    )
    right_frame_heading.pack(fill='x')

    # Total Product Label (Left Side)
    total_product_label = tk.Label(
        right_frame,
        text="Total Product:\t\t 0",
        font=("Times New Roman", 12, "italic"),
        bg=COLORS["background"],
        fg=COLORS["text"],
    )
    total_product_label.pack(pady=10, anchor='w')

    # Total Price Label (Right Side)
    total_price_label = tk.Label(
        right_frame,
        text="Total Price:\t\t Rs. 0",
        font=("Times New Roman", 12, "italic"),
        bg=COLORS["background"],
        fg=COLORS["text"],
        pady=5
    )
    total_price_label.pack(anchor='w')

    discount_label = tk.Label(right_frame, text="Discount in percentage", font=("Times New Roman", 14, "bold",),
                              bg=COLORS["background"], fg=COLORS["text"])
    discount_label.pack(anchor='w', pady=10, padx=20)

    discount_entry = tk.Entry(right_frame, width=18, font=("Times New Roman", 12),
                              bg="lightyellow", fg="black")
    discount_entry.pack(anchor='w', pady=20, padx=20)

    generate_bill_button = tk.Button(right_frame, text="Generate Bill", font=("Times New Roman", 14, "bold"),
                                     cursor="hand2",
                                     fg=COLORS["text"], bg=COLORS["background"], width=12,
                                     command=lambda: generate_bill(customer_name_entry, contact_number_entry,
                                                                   discount_entry))

    generate_bill_button.pack(anchor='w', pady=20, padx=20)

    final_fill_frame = tk.Frame(right_frame)
    final_fill_frame.pack()
    # now this frame will include all the items to be sold, and all that

    billing_product_tree_view.bind("<ButtonRelease-1>", lambda event: select_from_product(event, product_id_entry))

    create_billing_table()
