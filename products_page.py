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

    category_combobox = ttk.Combobox(left_frame, width=23, font=("Times New Roman", 12), state="readonly")
    category_combobox.set("Empty")
    category_combobox.grid(row=1, column=1, padx=5, pady=13)

    supplier_label = tk.Label(left_frame, text="Supplier", font=("Times New Roman", 16, "bold"),
                              bg=COLORS["background"], fg=COLORS["text"])
    supplier_label.grid(row=2, column=0, padx=5, pady=13, sticky="w")

    supplier_combobox = ttk.Combobox(left_frame, width=23, font=("Times New Roman", 12), state="readonly")
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
                           fg=COLORS["text"], bg=COLORS["background"], width=5)

    add_button.grid(row=0, column=0, padx=10)

    update_button = tk.Button(button_frame, text="Update", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=5)

    update_button.grid(row=0, column=1, padx=10)

    delete_button = tk.Button(button_frame, text="Delete", font=("Times New Roman", 14, "bold"), cursor="hand2",
                              fg=COLORS["text"], bg=COLORS["background"], width=5)

    delete_button.grid(row=0, column=2, padx=10)

    clear_button = tk.Button(button_frame, text="Clear", font=("Times New Roman", 14, "bold"), cursor="hand2",
                             fg=COLORS["text"], bg=COLORS["background"], width=5)

    clear_button.grid(row=0, column=3, padx=10)

    search_frame = tk.LabelFrame(product_frame, text="Search Product", bg=COLORS["background"],
                                 font=("Times New Roman", 14), fg=COLORS["text"])
    search_frame.place(x=430, y=40)

    search_product_combobox = ttk.Combobox(search_frame, width=18, font=("Times New Roman", 12), state="readonly",
                                           values=("Category", "Supplier", "Name", "Status"))
    search_product_combobox.set("Select Search Option")
    search_product_combobox.grid(row=0, column=0, padx=5, pady=13)

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
