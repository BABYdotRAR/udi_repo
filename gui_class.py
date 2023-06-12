import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from qr_reader import get_data_from_qr


class GUI_UDI:

    def __init__(self):
        self.root = tk.Tk()

        self.config_root()

        self.gothic_ui_14_font = tkFont.Font(family='Yu Gothic UI Light', size=14)

        self.welcome_label = tk.Label(
            self.root,
            text="Bienvenido de nuevo, por favor selecciona una opción",
            font=self.gothic_ui_14_font
        )
        self.welcome_label.pack(padx=10, pady=10)

        self.form_frame = tk.Frame(self.root)

        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=1)
        self.form_frame.columnconfigure(2, weight=1)

        self.init_string_vars()

        self.service_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.service_var, 
            "Préstamo de computadora.", 
            "Préstamo de cañón.", 
            "Préstamo de control."
        )
        self.service_dropdown.config(font=self.gothic_ui_14_font)
        self.service_dropdown.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.control_label = tk.Label(
            self.form_frame,
            text="Seleccione el control a prestar:",
            font=self.gothic_ui_14_font
        )
        self.classroom_control_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.classroom_control_var, 
            "102", 
            "E-202", 
            "Lab 2"
        )
        self.classroom_control_dropdown.config(font=self.gothic_ui_14_font)

        self.projector_label = tk.Label(
            self.form_frame,
            text="Seleccione el número de cañón a prestar:",
            font=self.gothic_ui_14_font
        )
        self.projector_number_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.projector_number_var, 
            "1", 
            "2", 
            "3"
        )
        self.projector_number_dropdown.config(font=self.gothic_ui_14_font)

        self.form_frame.pack(padx=10, pady=10)

        self.continue_btn = tk.Button(
            self.root, 
            text="Siguiente", 
            font=self.gothic_ui_14_font,
            command=self.on_continue
        )
        self.continue_btn.pack(padx=20, pady=20)

        self.root.mainloop()


    def config_root(self):
        self.root.title("UDI ESIT")
        self.root.geometry("800x600")


    def init_string_vars(self):
        self.service_var = tk.StringVar()
        self.service_var.trace("w", self.on_dropdown_changed)

        self.classroom_control_var = tk.StringVar()
        self.projector_number_var = tk.StringVar()


    def on_continue(self):
        qr_data = "Datos del QR: " + get_data_from_qr()
        service = "Servicio solicitado: \t" + self.service_var.get() 
        if self.service_var.get() == "Préstamo de control.":
            messagebox.showinfo(title="Datos recopilados",message=qr_data + "\n" + service + "\nSalón del control prestado:\t" + self.classroom_control_var.get())
        elif self.service_var.get() == "Préstamo de cañón.":
            messagebox.showinfo(title="Datos recopilados",message=qr_data + "\n" + service + "\nNúmero del cañón prestado:\t" + self.projector_number_var.get())
        else:
            messagebox.showinfo(title="Datos recopilados",message=qr_data + "\n" + service)


    def on_dropdown_changed(self, *args):
        option = self.service_var.get()

        if option == "Préstamo de cañón.":
            self.projector_label.grid(row=0, column=1, sticky=tk.W+tk.E)
            self.projector_number_dropdown.grid(row=0, column=2, sticky=tk.W+tk.E)

            self.control_label.grid_forget()
            self.classroom_control_dropdown.grid_forget()
        elif option == "Préstamo de control.":
            self.control_label.grid(row=0, column=1, sticky=tk.W+tk.E)
            self.classroom_control_dropdown.grid(row=0, column=2, sticky=tk.W+tk.E)

            self.projector_label.grid_forget()
            self.projector_number_dropdown.grid_forget()
        else:
            self.control_label.grid_forget()
            self.classroom_control_dropdown.grid_forget()
            self.projector_label.grid_forget()
            self.projector_number_dropdown.grid_forget()


GUI_UDI()

