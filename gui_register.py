import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from tkinter import messagebox

from qr_generator import create_img
from whatsapp_handler import send_img
from email_handler import send_email_with_image
import colors as color
import string_validator as str_val
import env_variables as env
import db_driver as db

class register_GUI():
    def __init__(self):
        self.root = tk.Toplevel()
        self.config_root()

        self.gothic_ui_light_14_font = font.Font(family='Yu Gothic UI Light', size=14)
        self.gothic_ui_16_font = font.Font(family='Yu Gothic UI bold', size=16)

        self.s = ttk.Style()
        self.s.configure('.', font=self.gothic_ui_light_14_font)

        self.title_label = ttk.Label(
            self.root,
            text="Registro de un nuevo usuario.", 
            foreground=color.white,
            background=color.dark_grey,
            font=self.gothic_ui_16_font
        )
        self.title_label.pack(pady=10)

        self.register_frame = tk.Frame(self.root)
        self.config_frame()

        self.init_string_vars()

        self.name_label = ttk.Label(
            self.register_frame,
            text="Nombre:", 
            foreground=color.white,
            background=color.dark_grey,
            font=self.gothic_ui_light_14_font
        )
        self.name_label.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)
        self.name_entry = ttk.Entry(
            self.register_frame, 
            textvariable=self.name,
            font=self.gothic_ui_light_14_font
        )
        self.name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=10, pady=10)

        self.lastname_label = ttk.Label(
            self.register_frame,
            text="Apellido:", 
            foreground=color.white,
            background=color.dark_grey,
            font=self.gothic_ui_light_14_font
        )
        self.lastname_label.grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)
        self.lastname_entry = ttk.Entry(
            self.register_frame, 
            textvariable=self.lastname,
            font=self.gothic_ui_light_14_font
        )
        self.lastname_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=10, pady=10)

        self.id_label = ttk.Label(
            self.register_frame,
            text="Boleta:", 
            foreground=color.white,
            background=color.dark_grey,
            font=self.gothic_ui_light_14_font
        )
        self.id_label.grid(row=2, column=0, sticky=tk.E, padx=10, pady=10)
        self.id_entry = ttk.Entry(
            self.register_frame, 
            textvariable=self.id,
            font=self.gothic_ui_light_14_font
        )
        self.id_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=10, pady=10)

        self.qr_send_option_label = ttk.Label(
            self.register_frame,
            text="Método para el envío del QR:", 
            foreground=color.white,
            background=color.dark_grey,
            font=self.gothic_ui_light_14_font
        )
        self.qr_send_option_label.grid(row=3, column=0, sticky=tk.E, padx=10, pady=10)
        self.qr_send_option_dropdown = ttk.OptionMenu(
            self.register_frame, 
            self.qr_option, 
            "Escoja una opción", 
            "Mensaje por Whatsapp", "Correo electrónico"
        )
        self.qr_send_option_dropdown.grid(row=3, column=1, sticky=tk.E, padx=10, pady=10)

        self.phone_number_label = ttk.Label(
            self.register_frame,
            text="Teléfono (+52):", 
            foreground=color.white,
            background=color.dark_grey,
            font=self.gothic_ui_light_14_font
        )
        self.phone_number_entry = ttk.Entry(
            self.register_frame, 
            textvariable=self.phone_number,
            font=self.gothic_ui_light_14_font
        )
        
        self.email_label = ttk.Label(
            self.register_frame,
            text="Correo electrónico:", 
            foreground=color.white,
            background=color.dark_grey,
            font=self.gothic_ui_light_14_font
        )
        self.email_entry = ttk.Entry(
            self.register_frame, 
            textvariable=self.email,
            font=self.gothic_ui_light_14_font
        )
        
        self.register_btn = ttk.Button(
            self.register_frame, 
            text="Registrar.", 
            command=self.on_register
        )
        self.register_btn.grid(row=5, column=1, sticky=tk.W, padx=10, pady=10)

        self.register_frame.pack(padx=20, pady=20, fill='both')

        self.root.mainloop()


    def config_root(self):
        self.root.geometry("800x600")
        self.root.title("Registro alumno.")
        self.root.config(bg=color.dark_grey)


    def config_frame(self):
        self.register_frame.columnconfigure(0, weight=1)
        self.register_frame.columnconfigure(1, weight=1)
        self.register_frame.config(bg=color.dark_grey)


    def init_string_vars(self):
        self.name = tk.StringVar()
        self.lastname = tk.StringVar()
        self.qr_option = tk.StringVar()
        self.qr_option.trace("w", self.on_dropdown_changed)
        self.phone_number = tk.StringVar()
        self.email = tk.StringVar()
        self.id =tk.StringVar()


    def on_dropdown_changed(self, *args):
        opt = self.qr_option.get()

        if opt == "Mensaje por Whatsapp":
            self.phone_number_label.grid(row=4, column=0, sticky=tk.E, padx=10, pady=10)
            self.phone_number_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=10, pady=10)

            self.email_label.grid_forget()
            self.email_entry.grid_forget()
        elif opt == "Correo electrónico":
            self.email_label.grid(row=4, column=0, sticky=tk.E, padx=10, pady=10)
            self.email_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=10, pady=10)

            self.phone_number_label.grid_forget()
            self.phone_number_entry.grid_forget()


    def on_register(self):
        err_msg = self.validate_entries()
        qr_data = self.id.get()
        _phone_number = self.phone_number.get()
        _email = self.email.get()

        if err_msg != "":
            messagebox.showerror(title="Datos incompletos", message="Atienda lo que se solicita:\n"+err_msg)
        else:
            create_img(qr_data, qr_data)
            path = env.PROJECT_PATH + "\\img\\" + qr_data + ".jpg"
            number = "+52" + _phone_number
            
            if self.qr_option.get() == "Mensaje por Whatsapp":
                send_img(path, number)
            else:
                res = send_email_with_image(_email, path)
                if res != "OK":
                    messagebox.showerror(title="Error al enviar el correo", message=res)

            self.insert_user()
            self.root.destroy()
    

    def validate_entries(self):
        _id = self.id.get()
        _qr_opt = self.qr_option.get()
        _phone_number = self.phone_number.get()
        _email = self.email.get()
        _name = self.name.get()
        _last_name = self.lastname.get()

        _id_flag = _id == ""
        _qr_opt_flag = not (_qr_opt == "Mensaje por Whatsapp") and not (_qr_opt == "Correo electrónico")
        _phone_number_flag = str_val.contains_only_numbers(_phone_number) == False
        _email_flag = str_val.is_valid_email(_email) == False
        _name_flag = str_val.has_no_numbers_or_special_chars(_name) == False
        _last_name_flag = str_val.has_no_numbers_or_special_chars(_last_name) == False

        err_msg = ""
        if _id_flag:
            err_msg = err_msg + "Boleta: introduzca un valor.\n"
        if _qr_opt_flag:
            err_msg = err_msg + "Opción de envío: seleccione un valor.\n"
        if _phone_number_flag and _qr_opt == "Mensaje por Whatsapp":
            err_msg = err_msg + "Teléfono: inserte un número válido.\n"
        if _email_flag and _qr_opt == "Correo electrónico":
            err_msg = err_msg + "Correo electrónico: proporcione una dirección válida.\n"
        if _name_flag:
            err_msg = err_msg + "Nombre: ingrese un nombre válido.\n"
        if _last_name_flag:
            err_msg = err_msg + "Apellido: ingrese un apellido válido."
        
        return err_msg
    

    def insert_user(self):
        _id = self.id.get()
        _phone_number = self.phone_number.get()
        _email = self.email.get()
        _name = self.name.get()
        _opt = 'phone' if self.qr_option.get() == "Mensaje por Whatsapp" else 'email'
        _last_name = self.lastname.get()
        _last_col = _phone_number if _opt == 'phone' else _email

        params = {"id": _id, "name":_name, "lastname":_last_name, 
                  "last_col":_last_col, "option":_opt}

        driver = db.DB_Driver()
        query_result = driver.create_new_user(params)

        if query_result == "OK":
            messagebox.showinfo(title="Usuario registrado", 
                                message="Usuario registrado correctamente, su código QR ha sido enviado al teléfono o correo proporcionado.")
        else:
            messagebox.showerror(title="Error en el registro", message=query_result)

        driver.close_connection()
