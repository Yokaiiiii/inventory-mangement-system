import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from employee import connect_database
from supplier_page import clear_supplier_field

COLORS = {
    "background": "#181C14",  # Dark background
    "frame": "#3C3D37",  # Sidebar and frames
    "highlight": "#697565",  # Subtitles, highlights
    "text": "#ECDFCC"  # Light text color for contrast
}


def create_table():
    connection, cursor = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_data (
            productid INT PRIMARY KEY AUTO_INCREMENT,
            category VARCHAR(100) NOT NULL,
            supplier VARCHAR(100) NOT NULL,
            name VARCHAR(150) NOT NULL UNIQUE, -- Ensures product names are unique
            price VARCHAR(50) NOT NULL CHECK (price >= 0), -- Prevents negative pricing
            quantity VARCHAR(20) NOT NULL CHECK (quantity >= 0), -- Prevents negative stock values
            status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active', -- Restricts status values
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically tracks creation time
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Auto-updates on modification
            );
        """)
        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        connection.close()


def fetch_category_option():
    category_option = []
    connection, cursor = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("SELECT name from category_data ")
        names = cursor.fetchall()
        for name in names:
            category_option.append(name[0])
        return category_option
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        connection.close()


def fetch_supplier_option():
    supplier_option = []
    connection, cursor = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("SELECT name from supplier_data ")
        names = cursor.fetchall()
        for name in names:
            supplier_option.append(name[0])
        return supplier_option
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        connection.close()


def add_product(category, supplier, name, price, quantity, status):
    if category == 'Empty' or supplier == 'Empty' or name == '' or price == '' or quantity == '' or status == 'Select Status':
        messagebox.showerror("Error", "Please fill all fields")
    else:
        connection, cursor = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("""
            INSERT INTO product_data ( category, supplier, name, price, quantity, status) VALUES (%s, %s, %s, %s, %s, %s)
            """, (category, supplier, name, price, quantity, status))
            connection.commit()

            treeview_data()
            messagebox.showinfo("Success", f"Product added to database")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            connection.close()


def clear_product_field(category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox,
                        check=False):
    category_combobox.set("Empty")
    supplier_combobox.set("Empty")
    name_entry.delete(0, "end")
    price_entry.delete(0, "end")
    quantity_entry.delete(0, "end")
    status_combobox.set("Select Status")
    if check:
        product_tree_view.selection_remove(product_tree_view.selection())


def select_product(event, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry,
                   status_combobox):
    index = product_tree_view.selection()
    content = product_tree_view.item(index[0])
    content = content["values"]

    clear_product_field(category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox)

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0, content[3])
    price_entry.insert(0, content[4])
    quantity_entry.insert(0, content[5])
    status_combobox.set(content[6])


def update_product(category, supplier, name, price, quantity, status):
    selected = product_tree_view.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a product")
    else:
        connection, cursor = connect_database()
        if not cursor or not connection:
            return
        try:
            index = product_tree_view.selection()
            content = product_tree_view.item(index[0])
            content = content["values"]
            product_id = content[0]
            cursor.execute("SELECT * FROM product_data WHERE productid = %s", (product_id,))
            current_data = cursor.fetchone()
            current_data = current_data[1:7]

            new_data = (category, supplier, name, price, quantity, status)
            print(current_data, new_data)
            if current_data == new_data:
                messagebox.showerror("Error", "No changes made before update")
                return

            cursor.execute("""
            UPDATE product_data SET category = %s, supplier = %s, name = %s, price = %s, quantity = %s, status = %s WHERE productid = %s
            """, (category, supplier, name, price, quantity, status, product_id))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", f"Product updated to database")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            connection.close()


def delete_product():
    selected = product_tree_view.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a product")
    else:
        connection, cursor = connect_database()
        if not cursor or not connection:
            return
        try:
            index = product_tree_view.selection()
            content = product_tree_view.item(index[0])
            content = content["values"]
            product_id = content[0]
            answer = messagebox.askyesno("Warning", "Are you sure you wanna delete the product?")

            if answer:
                cursor.execute("""
                DELETE FROM product_data WHERE productid = %s
                """, (product_id,))
                connection.commit()
                treeview_data()
                messagebox.showinfo("Success", f"Product deleted successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            connection.close()


def create_tree_view(height, width, frame, columns, x, y):
    treeview_frame = tk.Frame(frame, bg=COLORS["text"], height=height, width=width)
    treeview_frame.place(x=x, y=y)
    treeview_frame.propagate(False)  # Prevents resizing beyond defined width/height

    # Define columns with estimated widths

    # Create the Treeview
    product_tree_view = ttk.Treeview(
        treeview_frame, columns=list(columns.keys()), show="headings"
    )

    # Create Vertical Scrollbar
    tree_y_scroll = ttk.Scrollbar(treeview_frame, orient="vertical", command=product_tree_view.yview)
    product_tree_view.configure(yscrollcommand=tree_y_scroll.set)
    tree_y_scroll.pack(side="right", fill='y')  # Attach to right side

    # Create Horizontal Scrollbar
    tree_x_scroll = ttk.Scrollbar(treeview_frame, orient="horizontal", command=product_tree_view.xview)
    product_tree_view.configure(xscrollcommand=tree_x_scroll.set)
    tree_x_scroll.pack(side="bottom", fill="x")  # Attach to bottom

    # Pack the Treeview itself
    product_tree_view.pack(fill="both", expand=True)

    # Set column properties
    for key, (label, width) in columns.items():
        product_tree_view.heading(key, text=label)  # Set heading label
        product_tree_view.column(key, width=width, anchor="center")  # Optimize width & alignment

    return product_tree_view


def treeview_data():
    connection, cursor = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("SELECT * FROM product_data ORDER BY productid")
        product_records = cursor.fetchall()

        product_tree_view.delete(*product_tree_view.get_children())

        for record in product_records:
            product_tree_view.insert("", "end", values=record)
    except Exception as error:
        messagebox.showerror("Error", str(error))
    finally:
        cursor.close()
        connection.close()


# def select_product_field(event,  productid_entry,  )


def products_form(window):
    global back_button_icon, product_tree_view  # if we do not make this global, we do not get the back icon in the header
    # Create product management frame
    product_frame = tk.Frame(window, width=1020, height=567, bg=COLORS["background"])
    product_frame.place(x=251, y=112)

    # giving the top heading for the page
    product_heading_label = tk.Label(
        product_frame,
        text="Manage Product Details",
        font=("Times New Roman", 16, "bold"),
        bg=COLORS["text"],  # Light background for visibility
        fg=COLORS["background"],  # Dark text for contrast
    )
    product_heading_label.place(x=0, y=0, relwidth=1)

    # Back button to close the frame
    back_button_icon = tk.PhotoImage(file="./images/back.png")
    back_button = tk.Button(
        product_frame, image=back_button_icon, bd=0, cursor="hand2",
        bg=COLORS["text"], command=lambda: product_frame.place_forget()
    )
    back_button.place(x=5, y=0)

    left_frame = tk.Frame(product_frame, bg=COLORS["background"])
    left_frame.place(x=10, y=50)

    left_heading_label = tk.Label(
        left_frame,
        text="Manage Product Details",
        font=("Times New Roman", 22, "bold"),
        bg=COLORS["background"],  # Light background for visibility
        fg=COLORS["text"],  # Dark text for contrast
    )
    left_heading_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

    category_label = tk.Label(left_frame, text="Category", font=("Times New Roman", 16, "bold"),
                              bg=COLORS["background"], fg=COLORS["text"])
    category_label.grid(row=1, column=0, padx=5, pady=13, sticky="w")

    category_option = fetch_category_option()

    category_combobox = ttk.Combobox(left_frame, width=23, font=("Times New Roman", 12), state="readonly",
                                     values=category_option)
    category_combobox.set("Empty")
    category_combobox.grid(row=1, column=1, padx=5, pady=13)

    supplier_label = tk.Label(left_frame, text="Supplier", font=("Times New Roman", 16, "bold"),
                              bg=COLORS["background"], fg=COLORS["text"])
    supplier_label.grid(row=2, column=0, padx=5, pady=13, sticky="w")

    supplier_option = fetch_supplier_option()

    supplier_combobox = ttk.Combobox(left_frame, width=23, font=("Times New Roman", 12), state="readonly",
                                     values=supplier_option)
    supplier_combobox.set("Empty")
    supplier_combobox.grid(row=2, column=1, padx=5, pady=13)

    name_label = tk.Label(left_frame, text="Name", font=("Times New Roman", 16, "bold"),
                          bg=COLORS["background"], fg=COLORS["text"])
    name_label.grid(row=3, column=0, padx=5, pady=13, sticky="w")

    name_entry = tk.Entry(left_frame, width=25, font=("Times New Roman", 12),
                          bg="lightyellow", fg="black")
    name_entry.grid(row=3, column=1, padx=5, pady=13)

    price_label = tk.Label(left_frame, text="Price", font=("Times New Roman", 16, "bold"),
                           bg=COLORS["background"], fg=COLORS["text"])
    price_label.grid(row=4, column=0, padx=5, pady=13, sticky="w")

    price_entry = tk.Entry(left_frame, width=25, font=("Times New Roman", 12),
                           bg="lightyellow", fg="black")
    price_entry.grid(row=4, column=1, padx=5, pady=13)

    quantity_label = tk.Label(left_frame, text="Quantity", font=("Times New Roman", 16, "bold"),
                              bg=COLORS["background"], fg=COLORS["text"])
    quantity_label.grid(row=5, column=0, padx=5, pady=13, sticky="w")

    quantity_entry = tk.Entry(left_frame, width=25, font=("Times New Roman", 12),
                              bg="lightyellow", fg="black")
    quantity_entry.grid(row=5, column=1, padx=5, pady=13)

    status_label = tk.Label(left_frame, text="Status", font=("Times New Roman", 16, "bold"),
                            bg=COLORS["background"], fg=COLORS["text"])
    status_label.grid(row=6, column=0, padx=5, pady=13, sticky="w")

    status_combobox = ttk.Combobox(left_frame, width=23, font=("Times New Roman", 12), state="readonly",
                                   values=("Active", "Inactive"))
    status_combobox.set("Select Status")
    status_combobox.grid(row=6, column=1, padx=5, pady=13)

    button_frame = tk.Frame(left_frame, bg=COLORS["background"])
    button_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=13)

    add_button = tk.Button(button_frame, text="Add", font=("Times New Roman", 14, "bold"), cursor="hand2",
                           fg=COLORS["text"], bg=COLORS["background"], width=5,
                           command=lambda: add_product(category_combobox.get(), supplier_combobox.get(),
                                                       name_entry.get(),
                                                       price_entry.get(), quantity_entry.get(), status_combobox.get()))

    add_button.grid(row=0, column=0, padx=10)

    update_button = tk.Button(button_frame, text="Update", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=5,
                              command=lambda: update_product(category_combobox.get(), supplier_combobox.get(),
                                                             name_entry.get(),
                                                             price_entry.get(), quantity_entry.get(),
                                                             status_combobox.get()))

    update_button.grid(row=0, column=1, padx=10)

    delete_button = tk.Button(button_frame, text="Delete", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=5, command=delete_product)

    delete_button.grid(row=0, column=2, padx=10)

    clear_button = tk.Button(button_frame, text="Clear", font=("Times New Roman", 14, "bold"), cursor="hand2",
                             fg=COLORS["text"], bg=COLORS["background"], width=5,
                             command=lambda: clear_product_field(category_combobox, supplier_combobox,
                                                                 name_entry,
                                                                 price_entry, quantity_entry,
                                                                 status_combobox, True))

    clear_button.grid(row=0, column=3, padx=10)

    search_frame = tk.LabelFrame(product_frame, text="Search Product", bg=COLORS["background"],
                                 font=("Times New Roman", 14), fg=COLORS["text"])
    search_frame.place(x=430, y=40)

    search_supplier_combobox = ttk.Combobox(search_frame, width=18, font=("Times New Roman", 12), state="readonly",
                                            values=("Category", "product", "Name", "Status"))
    search_supplier_combobox.set("Select Search Option")
    search_supplier_combobox.grid(row=0, column=0, padx=5, pady=13)

    search_product_entry = tk.Entry(search_frame, width=18, font=("Times New Roman", 12),
                                    bg="lightyellow", fg="black")
    search_product_entry.grid(row=0, column=1, padx=5, pady=13)

    search_button = tk.Button(search_frame, text="Search", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=7)

    search_button.grid(row=0, column=2, padx=10)

    # Show all button
    show_all_button = tk.Button(search_frame, text="Show All", font=("Times New Roman", 14, "bold"), cursor="hand2",
                                fg=COLORS["text"], bg=COLORS["background"], width=7)

    show_all_button.grid(row=0, column=3, padx=10)

    product_tree_view_columns = {
        "productid": ("Product ID", 80),
        "category": ("Category", 100),
        "supplier": ("Supplier", 150),
        "name": ("Name", 100),
        "price": ("Price", 80),
        "quantity": ("Quantity", 80),
        "status": ("Status", 100),
        "created_at": ("Created At", 100),
        "updated_at": ("Updated At", 100),
    }
    product_tree_view = create_tree_view(height=400, width=563, frame=product_frame, columns=product_tree_view_columns,
                                         x=430, y=145);

    product_tree_view.bind("<ButtonRelease-1>",
                           lambda event: select_product(event, category_combobox, supplier_combobox, name_entry,
                                                        price_entry, quantity_entry, status_combobox))

    treeview_data()
    create_table()

    return product_frame
