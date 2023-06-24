import tkinter as tk
from tkinter import messagebox

from env_variables import DEV_EMAIL
from email_handler import send_email_with_body


class GUI_Issue:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Reportar un problema con la aplicación")
        
        self.textbox = tk.Text(self.root, height=7, width=70)
        self.textbox.pack(expand=1)

        self.send_btn = tk.Button(self.root, text="Enviar reporte", command=self.on_send)
        self.send_btn.pack()

        self.root.mainloop()

    
    def on_send(self):
        report = self.textbox.get("1.0", tk.END)
        res = send_email_with_body(DEV_EMAIL, report)
        if res != "OK":
            messagebox.showerror(title="Error al enviar el correo", message=res+"\nPor favor intente más tarde.", parent=self.root)
        else:
            messagebox.showinfo(title="Reporte enviado", message="Gracias. Tu reporte ha sido enviado al desarrollador y se buscará una solución.", parent=self.root)
        self.root.destroy()

