import tkinter as tk
import tkinter.ttk as ttk
from datetime import date
from tkinter import messagebox

import pymysql
from tkcalendar import DateEntry


def connect_database():
    try:
        connection = pymysql.connect(host="localhost", user="learningYokai", password="Le@rning123")
        cursor = connection.cursor()
    except:
        messagebox.showerror("Database Error", "Database Connection Error")
        return None, None
    cursor.execute("""
                USE inventory_system;
            """)
    return connection, cursor


def create_database_table():
    connection, cursor = connect_database()
    cursor.execute("""
        CREATE DATABASE IF NOT EXISTS inventory_system;
        """)
    # print("Database Created")
    cursor.execute("""
            USE inventory_system;
        """)
    # print("Using database inventory_system")
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee_data (
                empid INT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                gender VARCHAR(50),
                dob VARCHAR(50),
                contact VARCHAR(30),
                employment_type VARCHAR(50),
                education VARCHAR(50),
                work_shift VARCHAR(50),
                address VARCHAR(150),
                doj VARCHAR(50),
                salary VARCHAR(30),
                usertype VARCHAR(100),
                password VARCHAR(50)
                )
                """)
    # print("Table created successfully")


def treeview_data():
    connection, cursor = connect_database()
    if not connection and not cursor:
        return
    try:
        cursor.execute("SELECT * FROM employee_data");
        employee_records = cursor.fetchall()
        # since we are inserting (appending) to the tree view, so now we have to delete the previously added data and rewrite with the new data (instead of appending, ew are deleting pre data and again adding everything, yes it does increase overhead but we don't care about that right now)
        employee_tree_view.delete(
            *employee_tree_view.get_children())  # this deletes the previously stored data in the tree view, to not get duplicated data
        for record in employee_records:
            employee_tree_view.insert("", "end", values=record)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
    finally:
        connection.close()
        cursor.close()


def add_employee_command(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                         salary, usertype,
                         password):
    # print(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
    # usertype, password)

    if empid == '' or name == '' or email == '' or gender == 'Select Gender' or contact == '' or employment_type == '' or education == 'Select Education' or work_shift == 'Select Work Shift' or address == '' or salary == '' or usertype == 'Select User Type' or password == '':
        messagebox.showerror(title="Error", message="Please fill all fields")
    else:
        connection, cursor = connect_database()
        if not connection and not cursor:
            return
        try:
            cursor.execute("SELECT empid FROM employee_data WHERE empid = %s", (empid,))
            if cursor.fetchone():
                messagebox.showerror(title="Error", message="Employee ID already exists")
                return
            cursor.execute("""
            INSERT INTO employee_data VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s )
            """, (empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                  salary, usertype,
                  password))

            connection.commit()
            treeview_data()
            messagebox.showinfo(title="Success", message="Employee added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            connection.close()
            cursor.close()


def clear_field_command(empid_entry,
                        name_entry,
                        email_entry,
                        gender_combobox,
                        dob_entry,
                        contact_entry,
                        employment_type_combobox,
                        education_combobox,
                        work_shift_combobox,
                        address_text,
                        doj_entry,
                        salary_entry,
                        usertype_combobox,
                        password_entry, check=False):
    empid_entry.delete(0, "end")
    name_entry.delete(0, "end")
    email_entry.delete(0, "end")
    gender_combobox.set("Select Gender")
    dob_entry.set_date(date.today())  # Ensure dob_entry supports set_date()
    contact_entry.delete(0, "end")
    employment_type_combobox.set("Select Employment Type")  # Fixed value
    education_combobox.set("Select Education")  # Fixed value
    work_shift_combobox.set("Select Work Shift")
    address_text.delete("1.0", "end")  # Fixed for Text widget
    doj_entry.set_date(date.today())  # Ensure doj_entry supports set_date()
    salary_entry.delete(0, "end")
    usertype_combobox.set("Select User Type")
    password_entry.delete(0, "end")
    if check:
        employee_tree_view.selection_remove(employee_tree_view.selection())


def select_data(event, empid_entry,
                name_entry,
                email_entry,
                gender_combobox,
                dob_entry,
                contact_entry,
                employment_type_combobox,
                education_combobox,
                work_shift_combobox,
                address_text,
                doj_entry,
                salary_entry,
                usertype_combobox,
                password_entry):
    index = employee_tree_view.selection()
    content = employee_tree_view.item(index)
    content = content["values"]
    clear_field_command(empid_entry,
                        name_entry,
                        email_entry,
                        gender_combobox,
                        dob_entry,
                        contact_entry,
                        employment_type_combobox,
                        education_combobox,
                        work_shift_combobox,
                        address_text,
                        doj_entry,
                        salary_entry,
                        usertype_combobox,
                        password_entry)
    empid_entry.insert(0, content[0])
    name_entry.insert(0, content[1])
    email_entry.insert(0, content[2])
    gender_combobox.set(content[3])
    dob_entry.set_date(content[4])
    contact_entry.insert(0, content[5])
    employment_type_combobox.set(content[6])
    education_combobox.set(content[7])
    work_shift_combobox.set(content[8])
    address_text.insert(1.0, content[9])
    doj_entry.set_date(content[10])
    salary_entry.insert(0, content[11])
    usertype_combobox.set(content[12])
    password_entry.insert(0, content[13])


def update_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                    salary, usertype,
                    password):
    selected = employee_tree_view.selection()
    if not selected:
        messagebox.showerror("Error", "No row is selected")
    else:
        connection, cursor = connect_database()
        if not connection and not cursor:
            return
        try:
            cursor.execute("""
            SELECT * FROM employee_data WHERE empid = %s
            """, (empid,))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            # print(current_data)

            new_data = (name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                        salary, usertype,
                        password)

            if current_data == new_data:
                messagebox.showerror("Error", "No changed made before updating")
                return

            cursor.execute("""
            UPDATE employee_data SET name = %s, email = %s, gender = %s, dob = %s, contact = %s, employment_type = %s, education = %s, work_shift = %s, address = %s, doj = %s, salary = %s, usertype = %s, password = %s WHERE empid = %s
            """, (name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                  salary, usertype,
                  password, empid))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Employee updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            connection.close()
            cursor.close()


def delete_employee(empid):
    selected = employee_tree_view.selection()
    if not selected:
        messagebox.showerror("Error", "No row is selected")
    else:
        result = messagebox.askquestion("Delete Employee", "Are you sure you want to delete this employee?")
        if result == "yes":
            connection, cursor = connect_database()
            if not connection and not cursor:
                return
            try:
                cursor.execute("""
                DELETE FROM employee_data where empid = %s
                """, (empid,))
                connection.commit()
                treeview_data()
                messagebox.showinfo("Success", "Employee deleted")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                connection.close()
                cursor.close()


def search_employee(search_option, value):
    if search_option == "Search by":
        messagebox.showinfo("Search By", "Search Option is not selected")
    elif value == '':
        messagebox.showerror("Search By", "Enter a value to search")
    else:
        search_option = search_option.replace(" ", "_")
        connection, cursor = connect_database()
        if not connection or not cursor:
            return
        try:

            cursor.execute(f"SELECT * FROM employee_data WHERE {search_option} LIKE %s", f"%{value}%")
            records = cursor.fetchall()
            employee_tree_view.delete(*employee_tree_view.get_children())
            for record in records:
                employee_tree_view.insert("", "end", values=record)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            connection.close()
            cursor.close()


def show_all_command(search_combobox, search_entry):
    treeview_data()
    search_combobox.set("Search by")
    search_entry.delete(0, "end")


# Define color scheme for consistent theme
COLORS = {
    "background": "#181C14",  # Dark background
    "frame": "#3C3D37",  # Sidebar and frames
    "highlight": "#697565",  # Subtitles, highlights
    "text": "#ECDFCC"  # Light text color for contrast
}


def employee_form(window):
    global back_button_icon, employee_tree_view

    # Create employee management frame
    employee_frame = tk.Frame(window, width=1020, height=567, bg=COLORS["background"])
    employee_frame.place(x=251, y=112)

    # Header label
    employee_heading_label = tk.Label(
        employee_frame,
        text="Manage Employee Details",
        font=("Times New Roman", 16, "bold"),
        bg=COLORS["text"],  # Light background for visibility
        fg=COLORS["background"],  # Dark text for contrast
    )
    employee_heading_label.place(x=0, y=0, relwidth=1)

    # Back button to close the frame
    back_button_icon = tk.PhotoImage(file="./images/back.png")
    back_button = tk.Button(
        employee_frame, image=back_button_icon, bd=0, cursor="hand2",
        bg=COLORS["text"], command=lambda: employee_frame.place_forget()
    )
    back_button.place(x=5, y=0)

    top_frame = tk.Frame(employee_frame, bg=COLORS["background"])
    top_frame.place(x=0, y=35, relwidth=1, height=235)

    # this is for the search frame inside the top frame inside the employee frame
    search_frame = tk.Frame(top_frame, bg=COLORS["background"])
    search_frame.pack()

    search_combobox = ttk.Combobox(search_frame, values=(
        "EmpID", "Name", "Gender", "Email", "Contact", "Education", "Work Shift", "Salary", "Usertype",
        "Employment Type",
        "Address"),
                                   font=("Times New Roman", 12), state="readonly")
    search_combobox.set("Search by")
    search_combobox.configure(background="white", foreground="black")
    search_combobox.grid(row=0, column=0, padx=20)

    search_entry = tk.Entry(search_frame, width=40, bg="lightyellow", fg="black")
    search_entry.grid(row=0, column=1, padx=10)

    search_button = tk.Button(search_frame, text="Search", bg=COLORS["background"], fg="white", bd=0,
                              font=("Times New Roman", 12, "bold"), width=10, cursor="hand2",
                              command=lambda: search_employee(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=10)

    search_frame_show_all_button = tk.Button(search_frame, text="Show All", bg=COLORS["background"], fg="white", bd=0,
                                             font=("Times New Roman", 12, "bold"), width=10, cursor="hand2",
                                             command=lambda: show_all_command(search_combobox, search_entry))
    search_frame_show_all_button.grid(row=0, column=3, padx=10)

    employee_tree_view_columns = {
        "emp_id": ("EmpID", 80),
        "name": ("Name", 150),
        "email": ("Email", 200),
        "gender": ("Gender", 80),
        "dob": ("Date of Birth", 120),
        "contact": ("Contact Number", 140),
        "employment_type": ("Employment Type", 140),
        "education": ("Education", 120),
        "work_shift": ("Work Shift", 100),
        "doj": ("Date Of Join", 120),
        "salary": ("Salary", 100),
        "usertype": ("User Type", 100),
    }

    # Create the Treeview
    employee_tree_view = ttk.Treeview(
        top_frame, columns=list(employee_tree_view_columns.keys()), show="headings"
    )

    # Create Vertical Scrollbar
    tree_y_scroll = ttk.Scrollbar(top_frame, orient="vertical", command=employee_tree_view.yview)
    employee_tree_view.configure(yscrollcommand=tree_y_scroll.set)
    tree_y_scroll.pack(side="right", fill="y")  # Attach to right side

    # Create Horizontal Scrollbar
    tree_x_scroll = ttk.Scrollbar(top_frame, orient="horizontal", command=employee_tree_view.xview)
    employee_tree_view.configure(xscrollcommand=tree_x_scroll.set)
    tree_x_scroll.pack(side="bottom", fill="x")  # Attach to bottom

    # Pack the Treeview itself
    employee_tree_view.pack(pady=(15, 0), fill="both", expand=True)

    # Set column properties
    for key, (label, width) in employee_tree_view_columns.items():
        employee_tree_view.heading(key, text=label)  # Set heading label
        employee_tree_view.column(key, width=width, anchor="center")  # Optimize width & alignment

    treeview_data()  # calling this function so that it fetches all the entry in the database and show in the treeview

    detail_frame = tk.Frame(employee_frame, bg=COLORS["background"])
    detail_frame.place(x=5, y=275, height=285, width=1010)

    # Predefined options for dropdown fields
    gender_options = ["Male", "Female", "Other"]
    employment_type_options = ["Full-Time", "Part-Time", "Contract"]
    education_options = ["High School", "Bachelor's", "Master's", "PhD", "Other"]
    work_shift_options = ["Morning", "Evening", "Night"]
    usertype_options = ["Admin", "Employee", "Manager"]

    # Hardcoded entries for each field (static)
    empid_label = tk.Label(detail_frame, text="EmpID", font=("Times New Roman", 12, "bold"), bg=COLORS['background'],
                           fg=COLORS['text'])
    empid_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    empid_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
    empid_entry.grid(row=0, column=1, padx=10, pady=5)

    name_label = tk.Label(detail_frame, text="Name", font=("Times New Roman", 12, "bold"), bg=COLORS['background'],
                          fg=COLORS['text'])
    name_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
    name_entry.grid(row=0, column=3, padx=10, pady=5)

    email_label = tk.Label(detail_frame, text="Email", font=("Times New Roman", 12, "bold"), bg=COLORS['background'],
                           fg=COLORS['text'])
    email_label.grid(row=0, column=4, padx=10, pady=5, sticky="w")
    email_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
    email_entry.grid(row=0, column=5, padx=10, pady=5)

    # Gender dropdown
    gender_label = tk.Label(detail_frame, text="Gender", font=("Times New Roman", 12, "bold"), bg=COLORS['background'],
                            fg=COLORS['text'])
    gender_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    gender_combobox = ttk.Combobox(detail_frame, values=gender_options, state="readonly", width=19)
    gender_combobox.set("Select Gender")
    gender_combobox.grid(row=1, column=1, padx=10, pady=5)

    # Date of Birth field
    dob_label = tk.Label(detail_frame, text="Date of Birth", font=("Times New Roman", 12, "bold"),
                         bg=COLORS['background'], fg=COLORS['text'])
    dob_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
    dob_entry = DateEntry(detail_frame, width=19, height=3, font=("Times New Roman", 12), bg="lightyellow", fg="black",
                          state="readonly", date_pattern="dd/mm/yyyy")
    dob_entry.grid(row=1, column=3, padx=10, pady=5)

    # Contact field
    contact_label = tk.Label(detail_frame, text="Contact Number", font=("Times New Roman", 12, "bold"),
                             bg=COLORS['background'], fg=COLORS['text'])
    contact_label.grid(row=1, column=4, padx=10, pady=5, sticky="w")
    contact_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
    contact_entry.grid(row=1, column=5, padx=10, pady=5)

    # Employment Type dropdown
    employment_type_label = tk.Label(detail_frame, text="Employment Type", font=("Times New Roman", 12, "bold"),
                                     bg=COLORS['background'], fg=COLORS['text'])
    employment_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    employment_type_combobox = ttk.Combobox(detail_frame, values=employment_type_options, state="readonly", width=19)
    employment_type_combobox.set("Select Employment Type")
    employment_type_combobox.grid(row=2, column=1, padx=10, pady=5)

    # Education dropdown
    education_label = tk.Label(detail_frame, text="Education", font=("Times New Roman", 12, "bold"),
                               bg=COLORS['background'], fg=COLORS['text'])
    education_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
    education_combobox = ttk.Combobox(detail_frame, values=education_options, state="readonly", width=19)
    education_combobox.set("Select Education")
    education_combobox.grid(row=2, column=3, padx=10, pady=5)

    # Work Shift dropdown
    work_shift_label = tk.Label(detail_frame, text="Work Shift", font=("Times New Roman", 12, "bold"),
                                bg=COLORS['background'], fg=COLORS['text'])
    work_shift_label.grid(row=2, column=4, padx=10, pady=5, sticky="w")
    work_shift_combobox = ttk.Combobox(detail_frame, values=work_shift_options, state="readonly", width=19)
    work_shift_combobox.set("Select Work Shift")
    work_shift_combobox.grid(row=2, column=5, padx=10, pady=5)

    # Address field (Text widget)
    address_label = tk.Label(detail_frame, text="Address", font=("Times New Roman", 12, "bold"),
                             bg=COLORS['background'], fg=COLORS['text'])
    address_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    address_text = tk.Text(detail_frame, width=20, height=3, bg="lightyellow", fg="black", wrap="word")
    address_text.grid(row=3, column=1, padx=10, pady=5, rowspan=2)

    # Date of Joining field
    doj_label = tk.Label(detail_frame, text="Date Of Join", font=("Times New Roman", 12, "bold"),
                         bg=COLORS['background'], fg=COLORS['text'])
    doj_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")
    doj_entry = DateEntry(detail_frame, width=19, height=3, font=("Times New Roman", 12), bg="lightyellow", fg="black",
                          state="readonly", date_pattern="dd/mm/yyyy")
    doj_entry.grid(row=3, column=3, padx=10, pady=5)

    salary_label = tk.Label(detail_frame, text="Salary", font=("Times New Roman", 12, "bold"), bg=COLORS['background'],
                            fg=COLORS['text'])
    salary_label.grid(row=3, column=4, padx=10, pady=5, sticky="w")
    salary_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black")
    salary_entry.grid(row=3, column=5, padx=10, pady=5)

    # User Type dropdown
    usertype_label = tk.Label(detail_frame, text="User Type", font=("Times New Roman", 12, "bold"),
                              bg=COLORS['background'], fg=COLORS['text'])
    usertype_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")
    usertype_combobox = ttk.Combobox(detail_frame, values=usertype_options, state="readonly", width=19)
    usertype_combobox.set("Select User Type")
    usertype_combobox.grid(row=4, column=3, padx=10, pady=5)

    # Password field (Entry widget)
    password_label = tk.Label(detail_frame, text="Password", font=("Times New Roman", 12, "bold"),
                              bg=COLORS['background'], fg=COLORS['text'])
    password_label.grid(row=4, column=4, padx=10, pady=5, sticky="w")
    password_entry = tk.Entry(detail_frame, width=20, bg="lightyellow", fg="black", show="*")
    password_entry.grid(row=4, column=5, padx=10, pady=5)

    employee_button_frame = tk.Frame(detail_frame, bg=COLORS["background"])
    employee_button_frame.place(x=150, y=220)

    add_employee_button = tk.Button(employee_button_frame, text="Add Employee", bd=0, bg=COLORS["background"],
                                    fg=COLORS["text"], command=lambda: add_employee_command(empid_entry.get(),
                                                                                            name_entry.get(),
                                                                                            email_entry.get(),
                                                                                            gender_combobox.get(),
                                                                                            dob_entry.get(),
                                                                                            contact_entry.get(),
                                                                                            employment_type_combobox.get(),
                                                                                            education_combobox.get(),
                                                                                            work_shift_combobox.get(),
                                                                                            address_text.get("1.0",
                                                                                                             "end-1c"),
                                                                                            doj_entry.get(),
                                                                                            salary_entry.get(),
                                                                                            usertype_combobox.get(),
                                                                                            password_entry.get(),

                                                                                            # For multi-line text, use get("1.0", "end-1c")password_entry.get()

                                                                                            ))
    add_employee_button.grid(row=0, column=0, padx=20)

    update_employee_button = tk.Button(employee_button_frame, text="Update Employee", bd=0, bg=COLORS["background"],
                                       fg=COLORS["text"], command=lambda: update_employee(empid_entry.get(),
                                                                                          name_entry.get(),
                                                                                          email_entry.get(),
                                                                                          gender_combobox.get(),
                                                                                          dob_entry.get(),
                                                                                          contact_entry.get(),
                                                                                          employment_type_combobox.get(),
                                                                                          education_combobox.get(),
                                                                                          work_shift_combobox.get(),
                                                                                          address_text.get("1.0",
                                                                                                           "end-1c"),
                                                                                          doj_entry.get(),
                                                                                          salary_entry.get(),
                                                                                          usertype_combobox.get(),
                                                                                          password_entry.get(), ))
    update_employee_button.grid(row=0, column=1, padx=20)

    delete_employee_button = tk.Button(employee_button_frame, text="Delete Employee", bd=0, bg=COLORS["background"],
                                       fg=COLORS["text"], command=lambda: delete_employee(empid_entry.get(), ))
    delete_employee_button.grid(row=0, column=2, padx=20)

    clear_employee_button = tk.Button(employee_button_frame, text="Clear Employee", bd=0, bg=COLORS["background"],
                                      fg=COLORS["text"], command=lambda: clear_field_command(empid_entry,
                                                                                             name_entry,
                                                                                             email_entry,
                                                                                             gender_combobox,
                                                                                             dob_entry,
                                                                                             contact_entry,
                                                                                             employment_type_combobox,
                                                                                             education_combobox,
                                                                                             work_shift_combobox,
                                                                                             address_text,
                                                                                             doj_entry,
                                                                                             salary_entry,
                                                                                             usertype_combobox,
                                                                                             password_entry, True))
    clear_employee_button.grid(row=0, column=3, padx=20)

    employee_tree_view.bind('<ButtonRelease-1>', lambda event: select_data(event, empid_entry,
                                                                           name_entry,
                                                                           email_entry,
                                                                           gender_combobox,
                                                                           dob_entry,
                                                                           contact_entry,
                                                                           employment_type_combobox,
                                                                           education_combobox,
                                                                           work_shift_combobox,
                                                                           address_text,
                                                                           doj_entry,
                                                                           salary_entry,
                                                                           usertype_combobox,
                                                                           password_entry))

    create_database_table()
