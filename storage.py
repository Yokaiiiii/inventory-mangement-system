# # import tkinter as tk
# #
# # # Defining colors so that i can use the same color theme
# # color = ["#181C14", "#3C3D37", "#697565", "#ECDFCC"]
# #
# #
# # # functions part
# # def employeeForm():
# #     global back_button_icon
# #     employee_frame = tk.Frame(window, width=1070, height=567, bg=color[0])
# #     employee_frame.place(x=251, y=112)  # No extra indentation
# #
# #     employee_heading_label = tk.Label(
# #         employee_frame,
# #         text="Manage Employee Details",
# #         font=("Times New Roman", 16, "bold"),
# #         bg=color[3],
# #         fg=color[0],
# #     )
# #     employee_heading_label.place(x=0, y=0, relwidth=1)  # No extra indentation
# #
# #     back_button_icon = tk.PhotoImage(file="./images/back.png")
# #     back_button = tk.Button(employee_frame, image=back_button_icon, bd=0, cursor="hand2", bg=color[3],
# #                             command=lambda: employee_frame.place_forget())
# #
# #     back_button.place(x=5, y=0)
# #
# #
# # # This all is the GUI part
# # window = tk.Tk()
# #
# # window.geometry("1270x668")
# # window.title("Dashboard")
# # window.resizable(0, 0)  # used to disable maximize button
# # window.configure(bg=color[0])
# #
# # backgroundImage = tk.PhotoImage(file="./images/background.png")
# #
# # titleLabel = tk.Label(
# #     window,
# #     image=backgroundImage,
# #     compound="left",
# #     # anchor="w",
# #     text="Inventory management System",
# #     font=("times new roman", 40, "bold"),
# #     bg=color[0],
# #     fg=color[3],
# #     padx=20,
# # )
# # titleLabel.place(x=0, y=0, relwidth=1)
# # logoutButton = tk.Button(
# #     window,
# #     text="Logout",
# #     font=("Times New Roman", 20, "bold"),
# #     bg=color[0],  # Background color
# #     fg=color[3],  # Text color
# #     borderwidth=0,  # Remove the border
# #     relief="flat",  # Flat button style
# #     padx=20,  # Horizontal padding
# #     pady=10,  # Vertical padding
# #     highlightthickness=0,  # Remove highlight when clicked
# # )
# #
# # logoutButton.place(x=1100, y=10)
# #
# # subtitleLabel = tk.Label(
# #     window,
# #     text="Welcome Admin!!\t\t Date: 08-Feb-2015\t\t Time: 08:59 PM",
# #     bg=color[2],
# #     font=("time new roman", 15),
# #     fg=color[3],
# # )
# #
# # subtitleLabel.place(x=0, y=80, relwidth=1)
# #
# # leftFrame = tk.Frame(window, bg=color[1])
# # leftFrame.place(x=0, y=112, width=250, height=555)
# #
# # logoImage = tk.PhotoImage(file="./images/logo.png")
# # imageLabel = tk.Label(leftFrame, image=logoImage, bg=color[1])
# # # imageLabel.grid(row=0, column=0, padx=20, pady=10)
# # imageLabel.pack(pady=10)
# #
# # menuLabel = tk.Label(
# #     leftFrame,
# #     text="Menu",
# #     font=("Times New Roman", 30, "bold"),
# #     bg=color[3],
# #     fg=color[1],
# # )
# # menuLabel.pack(fill="x", pady=5)
# #
# # employee_icon = tk.PhotoImage(file="./images/employee.png")
# # employee_button = tk.Button(
# #     leftFrame,
# #     text="Employees",
# #     image=employee_icon,
# #     compound="left",
# #     anchor="w",
# #     font=("Times New Roman", 20),
# #     bg=color[3],
# #     fg=color[1],
# #     relief="flat",
# #     command=employeeForm
# # )
# # employee_button.pack(pady=1, fill="x")
# #
# # supplier_icon = tk.PhotoImage(file="./images/supplier.png")
# # supplier_button = tk.Button(
# #     leftFrame,
# #     text="Supplier",
# #     image=supplier_icon,
# #     compound="left",
# #     anchor="w",
# #     font=("Times New Roman", 20),
# #     bg=color[3],
# #     fg=color[1],
# #     relief="flat",
# # )
# # supplier_button.pack(pady=1, fill="x")
# #
# # category_icon = tk.PhotoImage(file="./images/category.png")
# # category_button = tk.Button(
# #     leftFrame,
# #     text="Category",
# #     image=category_icon,
# #     compound="left",
# #     anchor="w",
# #     font=("Times New Roman", 20),
# #     bg=color[3],
# #     fg=color[1],
# #     relief="flat",
# # )
# # category_button.pack(pady=1, fill="x")
# #
# # products_icon = tk.PhotoImage(file="./images/product.png")
# # products_button = tk.Button(
# #     leftFrame,
# #     text="Products",
# #     image=products_icon,
# #     compound="left",
# #     anchor="w",
# #     font=("Times New Roman", 20),
# #     bg=color[3],
# #     fg=color[1],
# #     relief="flat",
# # )
# # products_button.pack(pady=1, fill="x")
# #
# # sales_icon = tk.PhotoImage(file="./images/sales.png")
# # sales_button = tk.Button(
# #     leftFrame,
# #     text="Sales",
# #     image=sales_icon,
# #     compound="left",
# #     anchor="w",
# #     font=("Times New Roman", 20),
# #     bg=color[3],
# #     fg=color[1],
# #     relief="flat",
# # )
# # sales_button.pack(pady=1, fill="x")
# #
# # exit_icon = tk.PhotoImage(file="./images/exit.png")
# # exit_button = tk.Button(
# #     leftFrame,
# #     text="Exit",
# #     image=exit_icon,
# #     compound="left",
# #     anchor="w",
# #     font=("Times New Roman", 20),
# #     bg=color[3],
# #     fg=color[1],
# #     relief="flat",
# # )
# # exit_button.pack(pady=1, fill="x")
# #
# # emp_left_bar_frame = tk.Frame(window, bg=color[1])
# # emp_left_bar_frame.place(x=300, y=145, height=200, width=280)
# #
# # total_employee_icon = tk.PhotoImage(file="./images/total_emp.png")
# # total_employee_icon_label = tk.Label(
# #     emp_left_bar_frame, image=total_employee_icon, bg=color[1]
# # )
# # total_employee_icon_label.pack(pady=10)
# #
# # total_employee_label = tk.Label(
# #     emp_left_bar_frame,
# #     text="Total Employee",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 20, "bold"),
# # )
# # total_employee_label.pack(pady=5)
# #
# # total_employee_count_label = tk.Label(
# #     emp_left_bar_frame,
# #     text="0",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 40, "bold"),
# # )
# # total_employee_count_label.pack(pady=5)
# #
# # supplier_frame = tk.Frame(window, bg=color[1])
# # supplier_frame.place(x=615, y=145, height=200, width=280)
# #
# # total_supplier_icon = tk.PhotoImage(file="./images/total_sup.png")
# # total_supplier_icon_label = tk.Label(
# #     supplier_frame, image=total_supplier_icon, bg=color[1]
# # )
# # total_supplier_icon_label.pack(pady=10)
# #
# # total_supplier_label = tk.Label(
# #     supplier_frame,
# #     text="Total Supplier",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 20, "bold"),
# # )
# # total_supplier_label.pack(pady=5)
# #
# # total_supplier_count_label = tk.Label(
# #     supplier_frame,
# #     text="0",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 40, "bold"),
# # )
# # total_supplier_count_label.pack(pady=5)
# #
# # category_frame = tk.Frame(window, bg=color[1])
# # category_frame.place(x=930, y=145, height=200, width=280)
# #
# # total_category_icon = tk.PhotoImage(file="./images/total_cat.png")
# # total_category_icon_label = tk.Label(
# #     category_frame, image=total_category_icon, bg=color[1]
# # )
# # total_category_icon_label.pack(pady=10)
# #
# # total_category_label = tk.Label(
# #     category_frame,
# #     text="Total Category",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 20, "bold"),
# # )
# # total_category_label.pack(pady=5)
# #
# # total_category_count_label = tk.Label(
# #     category_frame,
# #     text="0",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 40, "bold"),
# # )
# # total_category_count_label.pack(pady=5)
# #
# # product_frame = tk.Frame(window, bg=color[1])
# # product_frame.place(x=450, y=370, height=200, width=280)
# #
# # total_product_icon = tk.PhotoImage(file="./images/total_prod.png")
# # total_product_icon_label = tk.Label(
# #     product_frame, image=total_product_icon, bg=color[1]
# # )
# # total_product_icon_label.pack(pady=10)
# #
# # total_product_label = tk.Label(
# #     product_frame,
# #     text="Total Category",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 20, "bold"),
# # )
# # total_product_label.pack(pady=5)
# #
# # total_product_count_label = tk.Label(
# #     product_frame,
# #     text="0",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 40, "bold"),
# # )
# # total_product_count_label.pack(pady=5)
# #
# # sales_frame = tk.Frame(window, bg=color[1])
# # sales_frame.place(x=800, y=370, height=200, width=280)
# #
# # total_sales_icon = tk.PhotoImage(file="./images/total_sales.png")
# # total_sales_icon_label = tk.Label(sales_frame, image=total_sales_icon, bg=color[1])
# # total_sales_icon_label.pack(pady=10)
# #
# # total_sales_label = tk.Label(
# #     sales_frame,
# #     text="Total Sales",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 20, "bold"),
# # )
# # total_sales_label.pack(pady=5)
# #
# # total_sales_count_label = tk.Label(
# #     sales_frame,
# #     text="0",
# #     bg=color[1],
# #     fg=color[3],
# #     font=("Times New Roman", 40, "bold"),
# # )
# # total_sales_count_label.pack(pady=5)
# #
# # window.mainloop()
#
# import tkinter as tk
# from tkinter import ttk
# from tkcalendar import DateEntry
#
# # Predefined options for dropdown fields
# gender_options = ["Male", "Female", "Other"]
# employment_type_options = ["Full-Time", "Part-Time", "Contract"]
# education_options = ["High School", "Bachelor's", "Master's", "PhD", "Other"]
# work_shift_options = ["Morning", "Evening", "Night"]
# usertype_options = ["Admin", "Employee", "Manager"]
#
# # COLORS for styling
# COLORS = {
#     "background": "#f4f4f4",
#     "text": "#000000"
# }
#
# # Initialize Tkinter window
# root = tk.Tk()
# root.title("Employee Form")
#
# # Frame to hold the form
# detail_frame = tk.Frame(root)
# detail_frame.grid(row=0, column=0, padx=10, pady=10)
#
# # Hardcoded entries for each field (static)
# empid_label = tk.Label(detail_frame, text="EmpID", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# empid_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
# empid_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
# empid_entry.grid(row=0, column=1, padx=10, pady=5)
#
# name_label = tk.Label(detail_frame, text="Name", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
# name_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
# name_entry.grid(row=1, column=1, padx=10, pady=5)
#
# email_label = tk.Label(detail_frame, text="Email", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# email_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
# email_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
# email_entry.grid(row=2, column=1, padx=10, pady=5)
#
# # Gender dropdown
# gender_label = tk.Label(detail_frame, text="Gender", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# gender_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
# gender_combobox = ttk.Combobox(detail_frame, values=gender_options, state="readonly", width=19)
# gender_combobox.grid(row=3, column=1, padx=10, pady=5)
#
# # Date of Birth field
# dob_label = tk.Label(detail_frame, text="Date of Birth", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# dob_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
# dob_entry = DateEntry(detail_frame, width=19, height=3, font=("Times New Roman", 12), bg="lightyellow", fg="black", state="readonly", date_pattern="dd/mm/yyyy")
# dob_entry.grid(row=4, column=1, padx=10, pady=5)
#
# contact_label = tk.Label(detail_frame, text="Contact Number", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# contact_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
# contact_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
# contact_entry.grid(row=5, column=1, padx=10, pady=5)
#
# # Employment Type dropdown
# employment_type_label = tk.Label(detail_frame, text="Employment Type", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# employment_type_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
# employment_type_combobox = ttk.Combobox(detail_frame, values=employment_type_options, state="readonly", width=19)
# employment_type_combobox.grid(row=6, column=1, padx=10, pady=5)
#
# # Education dropdown
# education_label = tk.Label(detail_frame, text="Education", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# education_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
# education_combobox = ttk.Combobox(detail_frame, values=education_options, state="readonly", width=19)
# education_combobox.grid(row=7, column=1, padx=10, pady=5)
#
# # Work Shift dropdown
# work_shift_label = tk.Label(detail_frame, text="Work Shift", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# work_shift_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
# work_shift_combobox = ttk.Combobox(detail_frame, values=work_shift_options, state="readonly", width=19)
# work_shift_combobox.grid(row=8, column=1, padx=10, pady=5)
#
# # Date of Joining field
# doj_label = tk.Label(detail_frame, text="Date Of Join", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# doj_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
# doj_entry = DateEntry(detail_frame, width=19, height=3, font=("Times New Roman", 12), bg="lightyellow", fg="black", state="readonly", date_pattern="dd/mm/yyyy")
# doj_entry.grid(row=9, column=1, padx=10, pady=5)
#
# salary_label = tk.Label(detail_frame, text="Salary", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# salary_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
# salary_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
# salary_entry.grid(row=10, column=1, padx=10, pady=5)
#
# # User Type dropdown
# usertype_label = tk.Label(detail_frame, text="User Type", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# usertype_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")
# usertype_combobox = ttk.Combobox(detail_frame, values=usertype_options, state="readonly", width=19)
# usertype_combobox.grid(row=11, column=1, padx=10, pady=5)
#
# # Address field (Text widget)
# address_label = tk.Label(detail_frame, text="Address", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# address_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")
# address_text = tk.Text(detail_frame, width=20, height=3, bg="lightyellow", fg="black", wrap="word")
# address_text.grid(row=12, column=1, padx=10, pady=5)
#
# # Password field (Entry widget)
# password_label = tk.Label(detail_frame, text="Password", font=("Times New Roman", 12, "bold"), bg=COLORS['background'], fg=COLORS['text'])
# password_label.grid(row=13, column=0, padx=10, pady=5, sticky="w")
# password_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black", show="*")
# password_entry.grid(row=13, column=1, padx=10, pady=5)
#
# root.mainloop()
#
