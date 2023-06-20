import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

import colors as color
import db_driver as db


class GUI_list:
    def __init__(self):
        self.root = tk.Toplevel()
        self.config_root()

        self.user_id_close_loan = "-1"
        self.driver = db.DB_Driver()
        self.treeview_columns = ('user_id', 'object_name')
        self.treeview_computer_loan_columns  = ('user_id',)
        self.gothic_ui_light_12_font = font.Font(family='Yu Gothic UI Light', size=12)
        self.gothic_ui_16_font = font.Font(family='Yu Gothic UI bold', size=16)

        self.welcome_label = tk.Label(
            self.root,
            text="Estos son los préstamos activos:",
            font=self.gothic_ui_16_font,
            fg=color.white,
            bg=color.dark_blue
        )
        self.welcome_label.pack(padx=10, pady=10)

        self.obj_loans_frame = tk.Frame(self.root)
        self.comp_loans_frame = tk.Frame(self.root)
        self.obj_loans_frame.config(bg=color.dark_blue)
        self.comp_loans_frame.config(bg=color.dark_blue)
        self.init_treeviews()
        self.obj_loans_frame.pack(padx=15, pady=15)
        self.comp_loans_frame.pack(padx=15, pady=15)

        self.end_loan_btn = tk.Button(
            self.root, 
            text="Terminar préstamo", 
            font=self.gothic_ui_light_12_font,
            bg=color.light_purple,
            fg=color.black, 
            borderwidth=0,
            command=self.on_close,
            padx=5,
            pady=5
        )
        self.end_loan_btn.pack(padx=20, pady=20)

        self.root.state('zoomed')
        self.root.mainloop()


    def config_root(self):
        self.root.title("Préstamos")
        self.root.geometry("800x600")
        self.root.config(bg=color.dark_blue)


    def init_treeviews(self):
        self.controls_label = tk.Label(
            self.obj_loans_frame,
            text="Controles en préstamo:",
            font=self.gothic_ui_light_12_font,
            fg=color.white,
            bg=color.dark_blue
        )
        self.controls_label.grid(padx=5, pady=5, column=0, row=0)
        self.controls_treeview = ttk.Treeview(
            self.obj_loans_frame, 
            columns=self.treeview_columns,
            show='headings'
        )
        self.controls_treeview.heading('user_id', text='Boleta')
        self.controls_treeview.heading('object_name', text='Aula')

        loaned_controls = self.driver.get_current_loaned_controls()

        for loan in loaned_controls:
            self.controls_treeview.insert('', tk.END, values=loan)

        self.controls_treeview.bind('<<TreeviewSelect>>', self.control_item_selected)
        self.controls_treeview.grid(row=1, column=0, sticky='nsew')

        self.projectors_label = tk.Label(
            self.obj_loans_frame,
            text="Proyectores en préstamo:",
            font=self.gothic_ui_light_12_font,
            fg=color.white,
            bg=color.dark_blue
        )
        self.projectors_label.grid(padx=5, pady=5, column=1, row=0)
        self.projectors_treeview = ttk.Treeview(
            self.obj_loans_frame, 
            columns=self.treeview_columns,
            show='headings'
        )
        self.projectors_treeview.heading('user_id', text='Boleta')
        self.projectors_treeview.heading('object_name', text='Proyector')

        loaned_projectors = self.driver.get_current_loaned_projectors()

        for loan in loaned_projectors:
            self.projectors_treeview.insert('', tk.END, values=loan)

        self.projectors_treeview.bind('<<TreeviewSelect>>', self.projectors_item_selected)
        self.projectors_treeview.grid(row=1, column=1, sticky='nsew')

        self.computers_label = tk.Label(
            self.comp_loans_frame,
            text="Préstamos de computadora:",
            font=self.gothic_ui_light_12_font,
            fg=color.white,
            bg=color.dark_blue
        )
        self.computers_label.grid(padx=5, pady=5, column=0, row=0)
        self.computers_treeview = ttk.Treeview(
            self.comp_loans_frame, 
            columns=self.treeview_computer_loan_columns,
            show='headings'
        )
        self.computers_treeview.heading('user_id', text='Boleta')

        loaned_computers = self.driver.get_current_loaned_computers()

        for loan in loaned_computers:
            self.computers_treeview.insert('', tk.END, values=loan)

        self.computers_treeview.bind('<<TreeviewSelect>>', self.computer_item_selected)
        self.computers_treeview.grid(row=1, column=0, sticky='nsew')
    

    def control_item_selected(self, event):
        for selected_item in self.controls_treeview.selection():
            item = self.controls_treeview.item(selected_item)
            self.user_id_close_loan = item['values'][0]
    

    def projectors_item_selected(self, event):
        for selected_item in self.projectors_treeview.selection():
            item = self.projectors_treeview.item(selected_item)
            self.user_id_close_loan = item['values'][0]


    def computer_item_selected(self, event):
        for selected_item in self.computers_treeview.selection():
            item = self.computers_treeview.item(selected_item)
            self.user_id_close_loan = item['values'][0]


    def on_close(self):
        _usr_id = self.user_id_close_loan

        if _usr_id == "-1":
            showerror(title="Error al cerrar préstamo", message="Seleccione un préstamo a cerrar.")
            return
        
        _res = self.driver.close_loan(_usr_id)

        if _res != "OK":
            showerror(title="Error al cerrar préstamo", message=_res)
            return
        
        self.destroy_treeviews()
        self.init_treeviews()
        showinfo(title="Préstamo concluido.", message="¡Listo! ;)\nTermina préstamo para: "+str(_usr_id))  


    def destroy_treeviews(self):
        self.controls_treeview.destroy()
        self.computers_treeview.destroy()
        self.projectors_treeview.destroy()


#GUI_list()
