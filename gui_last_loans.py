import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

import colors as color
import db_driver as db


class GUI_Last_Loans:
    def __init__(self):
        self.root = tk.Toplevel()
        self.config_root()
        self.driver = db.DB_Driver()
        self.init_fonts()

        self.welcome_label = self.create_label(self.root, "Estos son los últimos préstamos realizados:",
                                               self.gothic_ui_bold_16_font )
        self.welcome_label.pack(padx=10, pady=10)

        self.main_frame = self.create_frame(self.root, total_cols=1)
        self.init_treeviews()
        self.main_frame.pack(padx=10, pady=10, fill='y')

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
    

    def create_treeview(self, parent:tk.Frame, cols, headings, tree_values) -> ttk.Treeview:
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

        return treeview


    def init_fonts(self):
        self.gothic_ui_light_10_font = font.Font(family='Yu Gothic UI Light', size=10)
        self.gothic_ui_light_12_font = font.Font(family='Yu Gothic UI Light', size=12)
        self.gothic_ui_light_14_font = font.Font(family='Yu Gothic UI Light', size=14)
        self.gothic_ui_bold_14_font = font.Font(family='Yu Gothic UI bold', size=14)
        self.gothic_ui_bold_16_font = font.Font(family='Yu Gothic UI bold', size=16)


    def init_treeviews(self):
        last_loans = self.driver.get_last_loans()
        treeview_last_loan_columns = ('boleta', 'nombre', 'inicio', 'estado', 'dispositivo')

        self.last_loans_treeview = self.create_treeview(self.main_frame, 
                                                      treeview_last_loan_columns, 
                                                      treeview_last_loan_columns, last_loans)
        self.last_loans_treeview.grid(row=0, column=1, sticky='nsew')
        # verscrlbar = ttk.Scrollbar(self.main_frame,
        #                    orient ="vertical",
        #                    command = self.last_loans_treeview.yview)
        # verscrlbar.grid(row=0, column=1, sticky='nsew')
        # self.last_loans_treeview.configure(xscrollcommand=verscrlbar.set)


    def on_refresh(self):
        self.destroy_treeviews()
        self.init_treeviews()


    def destroy_treeviews(self):
        self.last_loans_treeview.destroy()
