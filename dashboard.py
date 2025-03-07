from category_page import *
from employee import employee_form
from products_page import products_form
from billing_page import billing_form
from supplier_page import supplier_form

import tkinter as tk
import time


def update_time():
    connection, cursor = connect_database()
    if not cursor or not connection:
        return

    # Fetch counts from database
    cursor.execute("SELECT count(empid) FROM employee_data")
    empid_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(productid) FROM product_data")
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(categoryid) FROM category_data")
    category_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(invoice) FROM supplier_data")
    supplier_count = cursor.fetchone()[0]

    cursor.execute("SELECT count(bill_id) FROM billing_data")
    sales_count = cursor.fetchone()[0]

    # print(f"Updated Stats - Employees: {empid_count}, Products: {product_count}, Categories: {category_count}, Suppliers: {supplier_count}")

    # Update count labels dynamically
    stats_labels["employees"].config(text=str(empid_count))
    stats_labels["suppliers"].config(text=str(supplier_count))
    stats_labels["categories"].config(text=str(category_count))
    stats_labels["products"].config(text=str(product_count))
    stats_labels["sales"].config(text=str(sales_count))

    # Update Date & Time in subtitle
    current_time = time.strftime("%I:%M %p")
    current_date = time.strftime("%d/%m/%Y")
    subtitle_label.config(text=f"Welcome Admin!!\t\t Date: {current_date}\t\t Time: {current_time}")

    # Refresh stats every 5 seconds
    window.after(5000, update_time)


current_frame = None


def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame = form_function(window)


# Define color scheme for consistent theme
COLORS = {
    "background": "#181C14",
    "frame": "#3C3D37",
    "highlight": "#697565",
    "text": "#ECDFCC"
}

# Initialize main application window
window = tk.Tk()
window.geometry("1270x668")
window.title("Dashboard")
window.resizable(0, 0)
window.configure(bg=COLORS["background"])

# Background Image
background_image = tk.PhotoImage(file="./images/background.png")

# Title label with background image
title_label = tk.Label(
    window, image=background_image, compound="left", text="Inventory Management System",
    font=("Times New Roman", 40, "bold"), bg=COLORS["background"], fg=COLORS["text"], padx=20
)
title_label.place(x=0, y=0, relwidth=1)

# Logout button
# logout_button = tk.Button(
#     window, text="Logout", font=("Times New Roman", 20, "bold"),
#     bg=COLORS["background"], fg=COLORS["text"], borderwidth=0, relief="flat", padx=20, pady=10
# )
# logout_button.place(x=1100, y=10)

# Subtitle label (Admin Welcome & Date/Time)
subtitle_label = tk.Label(
    window, text="Welcome Admin!!\t\t Date: 08-Feb-2015\t\t Time: 08:59 PM",
    bg=COLORS["highlight"], font=("Times New Roman", 15), fg=COLORS["text"]
)
subtitle_label.place(x=0, y=80, relwidth=1)

# Sidebar menu
left_frame = tk.Frame(window, bg=COLORS["frame"])
left_frame.place(x=0, y=112, width=250, height=555)

# Sidebar Logo
logo_image = tk.PhotoImage(file="./images/logo.png")
image_label = tk.Label(left_frame, image=logo_image, bg=COLORS["frame"])
image_label.pack(pady=10)

# Sidebar Menu Label
menu_label = tk.Label(
    left_frame, text="Menu", font=("Times New Roman", 30, "bold"),
    bg=COLORS["text"], fg=COLORS["frame"]
)
menu_label.pack(fill="x", pady=5)

# Sidebar buttons
menu_buttons = [
    ("Employees", "./images/employee.png", lambda: show_form(employee_form)),
    ("Supplier", "./images/supplier.png", lambda: show_form(supplier_form)),
    ("Category", "./images/category.png", lambda: show_form(category_form)),
    ("Products", "./images/product.png", lambda: show_form(products_form)),
    ("Billing", "./images/sales.png", lambda: show_form(billing_form)),
    ("Exit", "./images/exit.png", None)
]

for text, img_path, command in menu_buttons:
    icon = tk.PhotoImage(file=img_path)
    button = tk.Button(
        left_frame, text=text, image=icon, compound="left", anchor="w",
        font=("Times New Roman", 20), bg=COLORS["text"], fg=COLORS["frame"], relief="flat",
        command=command
    )
    button.image = icon  # Prevent garbage collection
    button.pack(pady=1, fill="x")


# Dashboard Stats Section
def create_stat_frame(x, y, icon_path, label_text):
    frame = tk.Frame(window, bg=COLORS["frame"])
    frame.place(x=x, y=y, height=200, width=280)

    icon = tk.PhotoImage(file=icon_path)
    icon_label = tk.Label(frame, image=icon, bg=COLORS["frame"])
    icon_label.image = icon  # Prevent garbage collection
    icon_label.pack(pady=10)

    text_label = tk.Label(
        frame, text=label_text, bg=COLORS["frame"], fg=COLORS["text"],
        font=("Times New Roman", 20, "bold")
    )
    text_label.pack(pady=5)

    count_label = tk.Label(
        frame, text="0", bg=COLORS["frame"], fg=COLORS["text"],
        font=("Times New Roman", 40, "bold")
    )
    count_label.pack(pady=5)

    return count_label  # Return count label for updates


# Dictionary to store count labels
stats_labels = {}

# Creating statistic frames & storing count labels
stats_labels["employees"] = create_stat_frame(300, 145, "./images/total_emp.png", "Total Employees")
stats_labels["suppliers"] = create_stat_frame(615, 145, "./images/total_sup.png", "Total Suppliers")
stats_labels["categories"] = create_stat_frame(930, 145, "./images/total_cat.png", "Total Categories")
stats_labels["products"] = create_stat_frame(450, 370, "./images/total_prod.png", "Total Products")
stats_labels["sales"] = create_stat_frame(800, 370, "./images/total_sales.png", "Total Sales")

# Start updating stats
update_time()

# Run the Tkinter main event loop
window.mainloop()
