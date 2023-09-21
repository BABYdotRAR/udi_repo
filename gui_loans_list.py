import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

import colors as color
import db_driver as db


class GUI_Current_Loans:
    def __init__(self):
        self.root = tk.Toplevel()
        self.config_root()

        self.user_id_close_loan = []
        self.driver = db.DB_Driver()
        self.init_fonts()

        self.welcome_label = self.create_label(self.root, "Estos son los préstamos activos:",
                                               self.gothic_ui_bold_16_font )
        self.welcome_label.pack(padx=10, pady=10)

        self.obj_loans_frame = self.create_frame(self.root, total_cols=2)
        self.comp_loans_frame = self.create_frame(self.root, total_cols=1)
        self.init_treeviews()
        self.obj_loans_frame.pack(padx=10, pady=10)
        self.comp_loans_frame.pack(padx=10, pady=10)

        self.end_loan_btn = self.create_button(self.root, self.on_close, "Terminar préstamo", 
                                               self.gothic_ui_light_14_font)
        self.end_loan_btn.pack(padx=10, pady=10, side='left')

        self.refresh_btn = self.create_button(self.root, self.on_refresh, "Refrescar", 
                                              self.gothic_ui_light_10_font)
        self.refresh_btn.pack(padx=10, pady=10, side='right')

        self.root.state('zoomed')
        self.root.mainloop()


    def config_root(self):
        self.root.title("Préstamos")
        self.root.geometry("800x600")
        self.root.config(bg=color.dark_blue)
    

    def create_frame(self, parent:tk.Frame, total_cols=3, background_color=color.dark_blue):
        frame = tk.Frame(parent)
        frame.config(bg=background_color)
        for i in range(total_cols):
            frame.columnconfigure(i, weight=1)
        return frame


    def create_label(self, parent:tk.Frame, label_text:str, label_font:font, 
                    text_color=color.white, background_color=color.dark_blue):
        lbl = tk.Label(
            parent,
            text=label_text,
            font=label_font,
            fg=text_color,
            bg=background_color
        )
        return lbl
    

    def create_button(self, parent:tk.Frame, btn_action, btn_text:str, btn_font:font, 
                      text_color=color.black, background_color=color.light_purple):
        btn = tk.Button(
            parent,
            text=btn_text,
            font=btn_font,
            command=btn_action,
            fg=text_color,
            bg=background_color,
            borderwidth=0,
            padx=5, pady=5
        )
        return btn
    

    def create_treeview(self, parent:tk.Frame, cols, headings, tree_values, bind_action):
        treeview = ttk.Treeview(
            parent,
            columns=cols,
            show='headings',
        )

        i = 0
        for txt_heading in headings:
            treeview.heading(cols[i], text=txt_heading)
            i = i + 1

        for v in tree_values:
            treeview.insert('', tk.END, values=v)

        #treeview.bind('<<TreeviewSelect>>', bind_action)
        return treeview


    def init_fonts(self):
        self.gothic_ui_light_10_font = font.Font(family='Yu Gothic UI Light', size=10)
        self.gothic_ui_light_12_font = font.Font(family='Yu Gothic UI Light', size=12)
        self.gothic_ui_light_14_font = font.Font(family='Yu Gothic UI Light', size=14)
        self.gothic_ui_bold_14_font = font.Font(family='Yu Gothic UI bold', size=14)
        self.gothic_ui_bold_16_font = font.Font(family='Yu Gothic UI bold', size=16)


    def init_treeviews(self):
        loaned_controls = self.driver.get_current_loaned_controls()
        loaned_projectors = self.driver.get_current_loaned_projectors()
        users_in_computer_loan = self.driver.get_current_users_in_computer_loan()
        treeview_obj_loan_columns = ('user_id', 'object_name')
        treeview_computer_loan_columns  = ('user_id',)

        self.controls_label = self.create_label(self.obj_loans_frame, 
                                                "Controles en préstamo:",
                                                self.gothic_ui_light_12_font)
        self.controls_label.grid(padx=5, pady=5, column=0, row=0, sticky="nsew")
        self.controls_treeview = self.create_treeview(self.obj_loans_frame, 
                                                      treeview_obj_loan_columns, 
                                                      ('Boleta', 'Aula'), loaned_controls, 
                                                      self.control_item_selected)
        self.controls_treeview.grid(row=1, column=0, sticky='nsew')

        self.projectors_label = self.create_label(self.obj_loans_frame, 
                                                  "Proyectores en préstamo:",
                                                  self.gothic_ui_light_12_font)
        self.projectors_label.grid(padx=5, pady=5, column=1, row=0, sticky="nsew")
        self.projectors_treeview = self.create_treeview(self.obj_loans_frame, 
                                                      treeview_obj_loan_columns, 
                                                      ('Boleta', 'Proyector'), 
                                                      loaned_projectors, 
                                                      self.projectors_item_selected)
        self.projectors_treeview.grid(row=1, column=1, sticky='nsew')

        self.computers_label = self.create_label(self.comp_loans_frame, 
                                                  "Préstamos de computadora:",
                                                  self.gothic_ui_light_12_font)
        self.computers_label.grid(padx=5, pady=5, column=0, row=0, sticky="nsew")
        self.computers_treeview = self.create_treeview(self.comp_loans_frame, 
                                                      treeview_computer_loan_columns, 
                                                      ('Boleta',), users_in_computer_loan, 
                                                      self.computer_item_selected)
        self.computers_treeview.grid(row=1, column=0, sticky='nsew')
    

    def control_item_selected(self):
        for selected_item in self.controls_treeview.selection():
            item = self.controls_treeview.item(selected_item)
            self.user_id_close_loan.append(item['values'][0])
        self.controls_treeview.selection_clear() 
    

    def projectors_item_selected(self):
        for selected_item in self.projectors_treeview.selection():
            item = self.projectors_treeview.item(selected_item)
            self.user_id_close_loan.append(item['values'][0]) 
        self.projectors_treeview.selection_clear()


    def computer_item_selected(self):
        for selected_item in self.computers_treeview.selection():
            item = self.computers_treeview.item(selected_item)
            self.user_id_close_loan.append(item['values'][0]) 


    def on_refresh(self):
        self.destroy_treeviews()
        self.init_treeviews()


    def on_close(self):
        self.control_item_selected()
        self.projectors_item_selected()
        self.computer_item_selected()
        if self.user_id_close_loan:
            for _id in self.user_id_close_loan:
                self.close_loan(_id)
            self.destroy_treeviews()
            self.init_treeviews()
            self.user_id_close_loan = []
        else:
            showerror(title="Error al cerrar préstamo", message="Seleccione al menos un préstamo a cerrar.", parent=self.root)


    def close_loan(self, _id):
        _usr_id = _id
        _res = self.driver.close_loan(_usr_id)

        if _res != "OK":
            showerror(title="Error al cerrar préstamo", message=_res, parent=self.root)
            return
        
        showinfo(title="Préstamo concluido.", message="¡Listo! ;)\nTermina préstamo para: "+str(_usr_id), parent=self.root)  


    def destroy_treeviews(self):
        self.controls_treeview.destroy()
        self.computers_treeview.destroy()
        self.projectors_treeview.destroy()

