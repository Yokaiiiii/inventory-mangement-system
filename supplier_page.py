import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from employee import connect_database

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
        CREATE TABLE IF NOT EXISTS supplier_data (
            invoice INT PRIMARY KEY ,  -- Unique identifier, auto-incremented
            name VARCHAR(100) NOT NULL,  -- Name is required
            contact VARCHAR(15) NOT NULL UNIQUE CHECK (LENGTH(contact) BETWEEN 10 AND 15),  -- Contact must be unique
            description VARCHAR(500) DEFAULT 'No description provided',  -- Default value for description
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Track record creation time
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP-- Auto-update timestamp
        )
        """)
        connection.commit()
    except Exception as error:
        messagebox.showerror("Error", str(error))
    finally:
        cursor.close()
        connection.close()


def add_supplier(invoice, name, contact, description):
    description = description.strip()
    invoice = invoice.strip()
    name = name.strip()
    contact = contact.strip()

    if "" in (invoice, name, contact, description):
        messagebox.showerror(title="Error", message="Please fill in all fields")
    else:
        connection, cursor = connect_database()

        if not cursor or not connection:
            return

        try:
            cursor.execute("SELECT invoice FROM supplier_data where invoice = %s", (invoice,))
            if cursor.fetchone():
                messagebox.showerror("Error", f"Invoice {invoice} already exists")
                return
            cursor.execute("INSERT INTO supplier_data (invoice,  name, contact, description) values (%s, %s, %s, %s)",
                           (invoice, name, contact, description))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", f"New invoice was added to the database")
        except Exception as error:
            messagebox.showerror("Error", str(error))
        finally:
            cursor.close()
            connection.close()


def clear_supplier_field(invoice_entry, name_entry, contact_entry, description_entry, check=False):
    invoice_entry.delete(0, "end")
    name_entry.delete(0, "end")
    contact_entry.delete(0, "end")
    description_entry.delete(1.0, "end")
    if check:
        supplier_tree_view.selection_remove(supplier_tree_view.selection())


def select_supplier_field(event, invoice_entry, name_entry, contact_entry, description_entry):
    index = supplier_tree_view.selection()
    content = supplier_tree_view.item(index[0])
    content = content["values"]

    clear_supplier_field(invoice_entry, name_entry, contact_entry, description_entry)

    invoice_entry.insert(0, content[0])
    name_entry.insert(0, content[1])
    contact_entry.insert(0, content[2])
    description_entry.insert(1.0, content[3])


def update_supplier_field(invoice, name, contact, description):
    selected = supplier_tree_view.selection()
    if not selected:
        messagebox.showerror("Error", f"Please select a supplier")
    else:
        connection, cursor = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("SELECT * FROM supplier_data where invoice = %s", (invoice,))
            current_data = cursor.fetchone()
            current_data = current_data[1:4]  # since the first value is the invoice and invoice will never be changed

            description = description.strip()
            new_data = (name, contact, description)
            print(current_data, new_data)

            if current_data == new_data:
                messagebox.showerror("Error", f"No changes made before updating")
                return

            # now this is the query for updating the database

            cursor.execute("""
            UPDATE supplier_data SET name = %s, contact = %s, description = %s WHERE invoice = %s
            """, (name, contact, description, invoice))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", f"Invoice {invoice} was updated")
        except Exception as error:
            messagebox.showerror("Error", str(error))
        finally:
            cursor.close()
            connection.close()


def delete_supplier_field(invoice):
    selected = supplier_tree_view.selection()
    if not selected:
        messagebox.showerror("Warning", "Please select a supplier")
    else:
        connection, cursor = connect_database()
        if not connection or not cursor:
            return
        try:
            answer = messagebox.askyesno("Warning", "Do you really want to delete this invoice?")
            if answer:
                cursor.execute("""
                DELETE FROM supplier_data where invoice = %s;
                """, (invoice,))
                connection.commit()
                treeview_data()

                messagebox.showinfo("Success", f"Invoice {invoice} was deleted")
        except Exception as error:
            messagebox.showerror("Error", str(error))
        finally:
            cursor.close()
            connection.close()


def search_supplier(invoice):
    if invoice == '':
        messagebox.showerror("Error", "Please enter an invoice value")
    else:
        connection, cursor = connect_database()
        if not connection or not cursor:
            return
        try:
            cursor.execute("SELECT * FROM supplier_data where invoice = %s", (invoice,))
            record = cursor.fetchone()
            if not record:
                messagebox.showerror("Searching Error", "Invoice does not exist")
                return
            supplier_tree_view.delete(*supplier_tree_view.get_children())
            supplier_tree_view.insert("", "end", values=record)

        except Exception as error:
            messagebox.showerror("Error", str(error))
        finally:
            cursor.close()
            connection.close()


def show_all_supplier(search_invoice_entry):
    treeview_data()
    search_invoice_entry.delete(0, "end")


def treeview_data():
    connection, cursor = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("SELECT * FROM supplier_data ORDER BY invoice")
        supplier_records = cursor.fetchall()

        supplier_tree_view.delete(*supplier_tree_view.get_children())

        for record in supplier_records:
            supplier_tree_view.insert("", "end", values=record)
    except Exception as error:
        messagebox.showerror("Error", str(error))
    finally:
        cursor.close()
        connection.close()


def supplier_form(window):
    global back_button_icon, supplier_tree_view  # if we do not make this global, we do not get the back icon in the header
    # Create Supplier management frame
    supplier_frame = tk.Frame(window, width=1020, height=567, bg=COLORS["background"])
    supplier_frame.place(x=251, y=112)

    # giving the top heading for the page
    supplier_heading_label = tk.Label(
        supplier_frame,
        text="Manage Employee Details",
        font=("Times New Roman", 16, "bold"),
        bg=COLORS["text"],  # Light background for visibility
        fg=COLORS["background"],  # Dark text for contrast
    )
    supplier_heading_label.place(x=0, y=0, relwidth=1)

    # Back button to close the frame
    back_button_icon = tk.PhotoImage(file="./images/back.png")
    back_button = tk.Button(
        supplier_frame, image=back_button_icon, bd=0, cursor="hand2",
        bg=COLORS["text"], command=lambda: supplier_frame.place_forget()
    )
    back_button.place(x=5, y=0)

    left_frame = tk.Frame(supplier_frame, bg=COLORS["background"])
    left_frame.place(x=15, y=75)

    # invoice number entry field

    invoice_label = tk.Label(left_frame, text="Invoice No.", font=("Times New Roman", 16, "bold"),
                             bg=COLORS["background"], fg=COLORS["text"])
    invoice_label.grid(row=0, column=0, padx=5, pady=13, sticky="w")

    invoice_entry = tk.Entry(left_frame, width=25, font=("Times New Roman", 12),
                             bg="lightyellow", fg="black")
    invoice_entry.grid(row=0, column=1, padx=5, pady=13)

    # Supplier name entry field
    supplier_name_label = tk.Label(left_frame, text="Supplier Name", font=("Times New Roman", 16, "bold"),
                                   bg=COLORS["background"], fg=COLORS["text"])
    supplier_name_label.grid(row=1, column=0, padx=5, pady=13, sticky="w")

    supplier_name_entry = tk.Entry(left_frame, width=25, font=("Times New Roman", 12), bg="lightyellow", fg="black")

    supplier_name_entry.grid(row=1, column=1, padx=5, pady=13)

    # Supplier contact entry field
    supplier_contact_label = tk.Label(left_frame, text="Contact", font=("Times New Roman", 16, "bold"),
                                      bg=COLORS["background"], fg=COLORS["text"])
    supplier_contact_label.grid(row=2, column=0, padx=5, pady=13, sticky="w")

    supplier_contact_entry = tk.Entry(left_frame, width=25, font=("Times New Roman", 12), bg="lightyellow", fg="black")

    supplier_contact_entry.grid(row=2, column=1, padx=5, pady=13)

    # Description of the product entry field

    description_label = tk.Label(left_frame, text="Description", font=("Times New Roman", 16, "bold"),
                                 bg=COLORS["background"], fg=COLORS["text"])
    description_label.grid(row=3, column=0, padx=5, pady=13, sticky="w")

    description_text = tk.Text(left_frame, width=25, height=4, bg="lightyellow", fg="black", wrap="word",
                               font=("Times New Roman", 12))
    description_text.grid(row=3, column=1, padx=5, pady=13)

    button_frame = tk.Frame(left_frame, bg=COLORS["background"])
    button_frame.grid(row=4, column=0, pady=(50, 0), columnspan=2)

    # Add button for supplier
    add_button = tk.Button(button_frame, text="Add", font=("Times New Roman", 14, "bold"), cursor="hand2",
                           fg=COLORS["text"], bg=COLORS["background"], width=7,
                           command=lambda: add_supplier(invoice_entry.get(), supplier_name_entry.get(),
                                                        supplier_contact_entry.get(),
                                                        description_text.get(1.0, 'end-1c')))

    add_button.grid(row=0, column=0, padx=10)

    # Update button for supplier
    update_button = tk.Button(button_frame, text="Update", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=7,
                              command=lambda: update_supplier_field(invoice_entry.get(), supplier_name_entry.get(),
                                                                    supplier_contact_entry.get(),
                                                                    description_text.get(1.0, 'end-1c')))

    update_button.grid(row=0, column=1, padx=10)

    # Delete button for supplier
    delete_button = tk.Button(button_frame, text="Delete", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=7,
                              command=lambda: delete_supplier_field(invoice_entry.get()))

    delete_button.grid(row=0, column=2, padx=10)

    # Clear button for supplier
    clear_button = tk.Button(button_frame, text="Clear", font=("Times New Roman", 14, "bold"), cursor="hand2",
                             fg=COLORS["text"], bg=COLORS["background"], width=7,
                             command=lambda: clear_supplier_field(invoice_entry, supplier_name_entry,
                                                                  supplier_contact_entry, description_text, True))

    clear_button.grid(row=0, column=3, padx=10)

    right_frame = tk.Frame(supplier_frame, bg=COLORS["background"])
    right_frame.place(x=500, y=75, height=450, width=500)

    search_frame = tk.Frame(right_frame, bg=COLORS["background"])
    search_frame.pack()

    # invoice number for searching in the right frame
    search_invoice_no_label = tk.Label(search_frame, text="Invoice No.", font=("Times New Roman", 16, "bold"),
                                       bg=COLORS["background"], fg=COLORS["text"])
    search_invoice_no_label.grid(row=0, column=0, padx=5, pady=13, sticky="w")

    search_invoice_entry = tk.Entry(search_frame, width=10, font=("Times New Roman", 14), bg="lightyellow", fg="black")
    search_invoice_entry.grid(row=0, column=1, padx=20, pady=13)

    # Search button
    search_button = tk.Button(search_frame, text="Search", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=7,
                              command=lambda: search_supplier(search_invoice_entry.get()))

    search_button.grid(row=0, column=2, padx=10)

    # Show all button
    show_all_button = tk.Button(search_frame, text="Show All", font=("Times New Roman", 14, "bold"), cursor="hand2",
                                fg=COLORS["text"], bg=COLORS["background"], width=7,
                                command=lambda: show_all_supplier(search_invoice_entry))

    show_all_button.grid(row=0, column=3, padx=10)
    # Define columns with estimated widths
    supplier_tree_view_columns = {
        "invoice": ("Invoice", 80),
        "name": ("Name", 100),
        "contact": ("Contact", 100),
        "description": ("Description", 200),
    }

    # Create the Treeview
    supplier_tree_view = ttk.Treeview(
        right_frame, columns=list(supplier_tree_view_columns.keys()), show="headings"
    )

    # Create Vertical Scrollbar
    tree_y_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=supplier_tree_view.yview)
    supplier_tree_view.configure(yscrollcommand=tree_y_scroll.set)
    tree_y_scroll.pack(side="right", fill='y', pady=(15, 0))  # Attach to right side

    # Create Horizontal Scrollbar
    tree_x_scroll = ttk.Scrollbar(right_frame, orient="horizontal", command=supplier_tree_view.xview)
    supplier_tree_view.configure(xscrollcommand=tree_x_scroll.set)
    tree_x_scroll.pack(side="bottom", fill="x")  # Attach to bottom

    # Pack the Treeview itself
    supplier_tree_view.pack(pady=(15, 0), fill="both", expand=True)

    # Set column properties
    for key, (label, width) in supplier_tree_view_columns.items():
        supplier_tree_view.heading(key, text=label)  # Set heading label
        supplier_tree_view.column(key, width=width, anchor="center")  # Optimize width & alignment

    supplier_tree_view.bind("<ButtonRelease-1>",
                            lambda event: select_supplier_field(event, invoice_entry, supplier_name_entry,
                                                                supplier_contact_entry, description_text))

    create_table()
    treeview_data()
    return supplier_frame
