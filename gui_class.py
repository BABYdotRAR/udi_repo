import tkinter as tk
from tkinter import font
from tkinter import messagebox

from qr_reader import get_data_from_qr
import colors as color
import db_driver as db


class GUI_UDI:

    def __init__(self):
        self.root = tk.Tk()

        self.config_root()
        self.driver = db.DB_Driver()

        self.gothic_ui_light_14_font = font.Font(family='Yu Gothic UI Light', size=14)
        self.gothic_ui_16_font = font.Font(family='Yu Gothic UI', size=16)

        self.welcome_label = tk.Label(
            self.root,
            text="Bienvenido de nuevo, por favor selecciona una opción",
            font=self.gothic_ui_16_font,
            fg=color.white,
            bg=color.dark_grey
        )
        self.welcome_label.pack(padx=10, pady=10)

        self.form_frame = tk.Frame(self.root)
        self.config_form_frame()

        self.init_string_vars()
        self.init_dropdowns()

        self.form_frame.pack(padx=10, pady=10, fill='x')

        self.continue_btn = tk.Button(
            self.root, 
            text="Siguiente", 
            font=self.gothic_ui_light_14_font,
            bg=color.aqua,
            fg=color.white, 
            borderwidth=0,
            command=self.on_continue
        )
        self.continue_btn.pack(side="right", padx=20, pady=20)

        self.root.mainloop()


    def config_root(self):
        self.root.title("UDI ESIT")
        self.root.geometry("800x600")
        self.root.config(bg=color.dark_grey)


    def config_form_frame(self):
        self.form_frame.config(bg=color.dark_grey)
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=1)
        self.form_frame.columnconfigure(2, weight=1)


    def init_string_vars(self):
        self.service_var = tk.StringVar()
        self.service_var.set("Escoja una opción")
        self.service_var.trace("w", self.on_dropdown_changed)

        self.classroom_control_var = tk.StringVar()
        self.classroom_control_var.set("Escoja una opción")
        self.projector_number_var = tk.StringVar()
        self.projector_number_var.set("Escoja una opción")


    def init_dropdowns(self):
        self.service_label = tk.Label(
            self.form_frame,
            text="Seleccione el servicio solicitado:",
            font=self.gothic_ui_light_14_font,
            fg=color.white,
            bg=color.dark_grey
        )
        self.service_label.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.services_dict = {"Préstamo de computadora":1, "Préstamo de proyector":2, "Préstamo de control remoto":3}
        self.service_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.service_var, 
            *self.services_dict.keys()
        )
        self.service_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.blue, fg=color.white, borderwidth=0)
        self.service_dropdown.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.control_label = tk.Label(
            self.form_frame,
            text="Seleccione el control a prestar:",
            font=self.gothic_ui_light_14_font,
            fg=color.white,
            bg=color.dark_grey
        )
        self.rmt_ctrls_list = self.driver.get_remote_controls()
        self.rmt_ctrls_dict = dict(self.rmt_ctrls_list)
        self.classroom_control_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.classroom_control_var, 
            *self.rmt_ctrls_dict.keys()
        )
        self.classroom_control_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.blue, fg=color.white, borderwidth=0)

        self.projector_label = tk.Label(
            self.form_frame,
            text="Seleccione el número de cañón a prestar:",
            font=self.gothic_ui_light_14_font,
            fg=color.white,
            bg=color.dark_grey
        )
        self.projectors = self.driver.get_projectors()
        self.projector_number_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.projector_number_var, 
            *self.projectors
        )
        self.projector_number_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.blue, fg=color.white, borderwidth=0)


    def on_continue(self):
        qr_data = "Datos del QR: " + get_data_from_qr()
        service = "Servicio solicitado: \t" + self.service_var.get() 
        if self.service_var.get() == "Préstamo de control remoto":
            messagebox.showinfo(title="Datos recopilados",message=qr_data + "\n" + service + "\nSalón del control prestado:\t" + self.classroom_control_var.get())
        elif self.service_var.get() == "Préstamo de proyector":
            messagebox.showinfo(title="Datos recopilados",message=qr_data + "\n" + service + "\nNúmero del cañón prestado:\t" + self.projector_number_var.get())
        else:
            messagebox.showinfo(title="Datos recopilados",message=qr_data + "\n" + service)


    def on_dropdown_changed(self, *args):
        option = self.service_var.get()

        if option == "Préstamo de proyector":
            self.projector_label.grid(row=2, column=1, sticky=tk.W+tk.E)
            self.projector_number_dropdown.grid(row=2, column=2, sticky=tk.W+tk.E)

            self.control_label.grid_forget()
            self.classroom_control_dropdown.grid_forget()
        elif option == "Préstamo de control remoto":
            self.control_label.grid(row=2, column=1, sticky=tk.W+tk.E)
            self.classroom_control_dropdown.grid(row=2, column=2, sticky=tk.W+tk.E)

            self.projector_label.grid_forget()
            self.projector_number_dropdown.grid_forget()
        else:
            self.control_label.grid_forget()
            self.classroom_control_dropdown.grid_forget()
            self.projector_label.grid_forget()
            self.projector_number_dropdown.grid_forget()


GUI_UDI()