import tkinter as tk
from tkinter import messagebox
from qr_generator import create_img

class register_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.config_root()

        self.title_label = tk.Label(text="Registro de un nuevo usuario.")
        self.title_label.pack(pady=10)

        self.register_frame = tk.Frame(self.root)
        self.config_frame()

        self.init_string_vars()

        self.name_label = tk.Label(
            self.register_frame,
            text="Ingrese su nombre:"
        )
        self.name_label.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.name_entry = tk.Entry(self.register_frame, textvariable=self.name)
        self.name_entry.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.lastname_label = tk.Label(
            self.register_frame,
            text="Ingrese su apellido:"
        )
        self.lastname_label.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.lastname_entry = tk.Entry(self.register_frame, textvariable=self.lastname)
        self.lastname_entry.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.id_label = tk.Label(
            self.register_frame,
            text="Ingrese su boleta:"
        )
        self.id_label.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.id_entry = tk.Entry(self.register_frame, textvariable=self.id)
        self.id_entry.grid(row=2, column=1, sticky=tk.W+tk.E)

        self.email_label = tk.Label(
            self.register_frame,
            text="Ingrese su correo:"
        )
        self.email_label.grid(row=3, column=0, sticky=tk.W+tk.E)
        self.email_entry = tk.Entry(self.register_frame, textvariable=self.email)
        self.email_entry.grid(row=3, column=1, sticky=tk.W+tk.E)

        self.register_btn = tk.Button(self.register_frame, text="Registrar.", command=self.on_register)
        self.register_btn.grid(row=4, column=1, sticky=tk.W+tk.E)

        self.register_frame.pack(padx=10, pady=10, fill='both')

        self.root.mainloop()


    def config_root(self):
        self.root.geometry("800x600")
        self.root.title("Registro alumno.")

    def config_frame(self):
        self.register_frame.columnconfigure(0, weight=1)
        self.register_frame.columnconfigure(1, weight=1)

    def init_string_vars(self):
        self.name = tk.StringVar()
        self.lastname = tk.StringVar()
        self.email = tk.StringVar()
        self.id =tk.StringVar()

    def on_register(self):
        qr_data = self.id.get()
        create_img(qr_data, qr_data)
        

register_GUI()