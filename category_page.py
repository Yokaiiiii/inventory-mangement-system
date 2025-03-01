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


def category_form(window):
    global back_button_icon, category_tree_view  # if we do not make this global, we do not get the back icon in the header
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
