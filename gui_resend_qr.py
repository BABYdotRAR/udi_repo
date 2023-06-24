import tkinter as tk
from tkinter import messagebox

from string_validator import is_valid_email
from email_handler import send_email_with_image
from qr_generator import create_img
import db_driver as db
import env_variables as env


class GUI_Resend_QR:
    def __init__(self):
        self.driver = db.DB_Driver()
        self.root = tk.Toplevel()
        self.root.title("Reenviar QR")
        self.root.geometry("250x100")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self.id = tk.StringVar()
        self.id_label = tk.Label(self.main_frame, text="Boleta:", padx=5, pady=5)
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(self.main_frame, textvariable=self.id)
        self.id_entry.grid(row=0, column=1)

        self.get_email_btn = tk.Button(self.main_frame, text="Siguiente", command=self.on_get_email)
        self.get_email_btn.grid(row=1, column=1)

        self.old_email = ""
        self.email = tk.StringVar()
        self.email_label = tk.Label(self.main_frame, text="Email:", padx=5, pady=5)
        self.email_entry = tk.Entry(self.main_frame, textvariable=self.email)
        self.send_qr_btn = tk.Button(self.main_frame, text="Enviar", command=self.on_resend_qr)

        self.main_frame.pack(fill='x')
        self.root.mainloop()

    
    def show_next_widgets(self):
        self.get_email_btn.grid_forget()
        self.email_label.grid(row=1, column=0)
        self.email_entry.grid(row=1, column=1, sticky=tk.W+tk.E)
        self.send_qr_btn.grid(row=2, column=0)

    
    def on_get_email(self):
        _retrieved_email = self.driver.get_email_by_user_id(self.id.get())

        if str(_retrieved_email).startswith("Error:"):
            messagebox.showerror(title="Ups! Algo salió mal", message=_retrieved_email, parent=self.root)
            return
        
        self.show_next_widgets()
        self.id_entry.config(state= "disabled")
        if _retrieved_email:
            self.email_entry.insert(0, _retrieved_email)
        self.old_email = _retrieved_email


    def on_resend_qr(self):
        _inserted_email = self.email.get()
        msg = ""

        if(is_valid_email(_inserted_email) == False):
            messagebox.showerror(title="Email inválido", message="Inserte un email válido", parent=self.root)
            return
        
        create_img(self.id.get(), self.id.get())
        img_path = env.PROJECT_PATH + "\\img\\" + self.id.get() + ".jpg"

        if(self.old_email != _inserted_email):
            self.driver.update_email_by_user_id(self.id.get(), _inserted_email)
            msg = "Su correo ha sido actualizado en la base de datos."

        res = send_email_with_image(_inserted_email, img_path)

        if res != "OK":
            messagebox.showerror(title="Ups! algo salió mal", message=res, parent=self.root)
            return
        
        msg = msg + "\nSe ha enviado el QR al correo proporcionado."
        messagebox.showinfo(title="Listo", message=msg)
        self.root.destroy()
        
