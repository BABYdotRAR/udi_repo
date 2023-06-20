import tkinter as tk
from tkinter import ttk

import colors as color
import db_driver as db


class GUI_list:
    def __init__(self):
        self.root = tk.Toplevel()
        self.config_root()

        self.driver = db.DB_Driver()
        self.treeview_columns = ('user_id', 'object_name')


    def config_root(self):
        self.root.title("UDI ESIT")
        self.root.geometry("800x600")
        self.root.config(bg=color.dark_blue)


    def init_treeviews(self):
        self.controls_treeview = ttk.Treeview(
            self.root, 
            columns=self.treeview_columns,
            show='headings'
        )
        self.controls_treeview.heading('user_id', 'Boleta')
        self.controls_treeview.heading('object_name', 'Aula')

        loaned_controls = self.driver.get_current_loaned_controls()

        for loan in loaned_controls:
            self.controls_treeview.insert('', tk.END, values=loan)
