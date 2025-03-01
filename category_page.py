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
        CREATE TABLE IF NOT EXISTS category_data (
            categoryid INT PRIMARY KEY, -- auto incrementer can be used here, but prefer not
            name varchar(100) NOT NULL,
            description varchar(500) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Track record creation time
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP-- Auto-update
        );
        """)
        connection.commit()
    except:
        messagebox.showerror("Error", "Failed to create table")
    finally:
        cursor.close()
        connection.close()


def clear_category_field(categoryid_entry, category_name_entry, category_description_entry, check=False):
    categoryid_entry.delete(0, "end")
    category_name_entry.delete(0, "end")
    category_description_entry.delete(1.0, "end")
    if check:
        category_tree_view.selection_remove(category_tree_view.selection())


def select_category_field(event, categoryid_entry, category_name_entry, category_description_entry):
    index = category_tree_view.selection()
    content = category_tree_view.item(index[0])
    content = content["values"]

    clear_category_field(categoryid_entry, category_name_entry, category_description_entry)

    categoryid_entry.insert(0, content[0])
    category_name_entry.insert(0, content[1])
    category_description_entry.insert(1.0, content[2])


def add_category(categoryid, category_name, category_description):
    if "" in (categoryid, category_name, category_description):
        messagebox.showerror("Error", "Please fill all the field")
    else:
        connection, cursor = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("SELECT categoryid FROM category_data WHERE categoryid = %s", (categoryid,))

            if cursor.fetchone():
                messagebox.showerror("Error", "Category already exists")
                return

            cursor.execute("INSERT INTO category_data (categoryid, name, description) VALUES (%s, %s, %s)",
                           (categoryid, category_name, category_description))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Category added")
        except:
            messagebox.showerror("Error", "Failed to add category")
        finally:
            cursor.close()
            connection.close()


def delete_category(categoryid):
    selected = category_tree_view.selection()
    if not selected:
        messagebox.showerror("Error", "No category selected")
    else:
        connection, cursor = connect_database()
        if not cursor or not connection:
            return
        else:
            try:
                answer = messagebox.askyesno("Warning", "Do you really want to delete this category? ")
                if answer:
                    cursor.execute("DELETE FROM category_data WHERE categoryid = %s", (categoryid,))
                    connection.commit()
                    treeview_data()
                    messagebox.showinfo("Success", "Category deleted")
            except:
                messagebox.showerror("Error", "Failed to delete category")
            finally:
                cursor.close()
                connection.close()


def treeview_data():
    connection, cursor = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("SELECT * FROM category_data ORDER BY categoryid")
        category_records = cursor.fetchall()

        category_tree_view.delete(*category_tree_view.get_children())

        for record in category_records:
            category_tree_view.insert("", "end", values=record)
    except:
        messagebox.showerror("Error", "Failed to get data from database")
    finally:
        cursor.close()
        connection.close()


def category_form(window):
    global back_button_icon, category_tree_view, category_image_logo  # if we do not make this global, we do not get the back icon in the header
    # Create category management frame
    category_frame = tk.Frame(window, width=1020, height=567, bg=COLORS["background"])
    category_frame.place(x=251, y=112)

    # giving the top heading for the page
    category_heading_label = tk.Label(
        category_frame,
        text="Manage Category Details",
        font=("Times New Roman", 16, "bold"),
        bg=COLORS["text"],  # Light background for visibility
        fg=COLORS["background"],  # Dark text for contrast
    )
    category_heading_label.place(x=0, y=0, relwidth=1)

    # Back button to close the frame
    back_button_icon = tk.PhotoImage(file="./images/back.png")
    back_button = tk.Button(
        category_frame, image=back_button_icon, bd=0, cursor="hand2",
        bg=COLORS["text"], command=lambda: category_frame.place_forget()
    )
    back_button.place(x=5, y=0)

    category_image_logo = tk.PhotoImage(file="./images/product_category.png")
    category_image_logo_label = tk.Label(category_frame, image=category_image_logo, bg=COLORS["background"])

    category_image_logo_label.place(x=30, y=80)

    right_frame = tk.Frame(category_frame, bg=COLORS["background"])
    right_frame.place(x=550, y=50)

    # Detail frame will include CategoryID, Category Name and Category description entry fields
    detail_frame = tk.Frame(right_frame, bg=COLORS["background"])
    detail_frame.pack()

    category_id_label = tk.Label(detail_frame, text="Category Id", bg=COLORS["background"], fg=COLORS["text"],
                                 font=("Times New Roman", 16, "bold"), padx=10, pady=10)
    category_id_label.grid(row=0, column=0, sticky="w")
    category_id_entry = tk.Entry(detail_frame, width=25, bg=COLORS["text"], fg="black")
    category_id_entry.grid(row=0, column=1, padx=10, pady=10)

    category_name_label = tk.Label(detail_frame, text="Category Name", bg=COLORS["background"], fg=COLORS["text"],
                                   font=("Times New Roman", 16, "bold"), padx=10, pady=10)
    category_name_label.grid(row=1, column=0, sticky="w")
    category_name_entry = tk.Entry(detail_frame, width=25, bg=COLORS["text"], fg="black")
    category_name_entry.grid(row=1, column=1, padx=10, pady=10)

    category_description_label = tk.Label(detail_frame, text="Description", bg=COLORS["background"],
                                          fg=COLORS["text"],
                                          font=("Times New Roman", 16, "bold"), padx=10, pady=10)
    category_description_label.grid(row=2, column=0, sticky="w")
    category_description_entry = tk.Text(detail_frame, width=25, height=3, bg=COLORS["text"], fg="black",
                                         font=("Times New Roman", 12))
    category_description_entry.grid(row=2, column=1, columnspan=2, rowspan=2, padx=10, pady=10)

    # Button frame will include Add and delete button
    button_frame = tk.Frame(right_frame, bg=COLORS["background"])
    button_frame.pack()

    add_category_button = tk.Button(button_frame, text="Add", bg=COLORS["background"], fg=COLORS["text"],
                                    font=("Times New Roman", 16, "bold"),
                                    command=lambda: add_category(category_id_entry.get(), category_name_entry.get(),
                                                                 category_description_entry.get(1.0, "end-1c")))
    add_category_button.grid(row=0, column=0, padx=10, pady=10)

    delete_category_button = tk.Button(button_frame, text="Delete", bg=COLORS["background"], fg=COLORS["text"],
                                       font=("Times New Roman", 16, "bold"),command=lambda: delete_category(category_id_entry.get()) )
    delete_category_button.grid(row=0, column=1, padx=10, pady=10)

    clear_category_button = tk.Button(button_frame, text="Clear", bg=COLORS["background"], fg=COLORS["text"],
                                      font=("Times New Roman", 16, "bold"),
                                      command=lambda: clear_category_field(category_id_entry, category_name_entry,
                                                                           category_description_entry, True))
    clear_category_button.grid(row=0, column=2, padx=10, pady=10)

    # Define Treeview column details (More readable format)
    category_tree_view_columns = {
        "categoryid": ("ID", 10),
        "name": ("Name", 100),
        "description": ("Description", 200),
    }

    # Create Treeview
    category_tree_view = ttk.Treeview(
        right_frame, columns=list(category_tree_view_columns.keys()), show="headings"
    )

    # Create and Pack Vertical Scrollbar
    tree_y_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=category_tree_view.yview)
    category_tree_view.configure(yscrollcommand=tree_y_scroll.set)
    tree_y_scroll.pack(side="right", fill="y", pady=(15, 0))  # Ensure it's visible

    # Create and Pack Horizontal Scrollbar
    tree_x_scroll = ttk.Scrollbar(right_frame, orient="horizontal", command=category_tree_view.xview)
    category_tree_view.configure(xscrollcommand=tree_x_scroll.set)
    tree_x_scroll.pack(side="bottom", fill="x")

    # Pack the Treeview
    category_tree_view.pack(pady=(15, 0), fill="both", expand=True)

    # Configure Treeview Columns
    for key, (label, width) in category_tree_view_columns.items():
        category_tree_view.heading(key, text=label)
        category_tree_view.column(key, width=width, anchor="center")

    treeview_data()
    category_tree_view.bind("<ButtonRelease-1>",
                            lambda event: select_category_field(event, category_id_entry, category_name_entry,
                                                                category_description_entry))

    create_table()
