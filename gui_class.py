import tkinter as tk
from tkinter import font
from tkinter import messagebox

from qr_reader import get_data_from_qr
from string_validator import extract_number
import colors as color
import db_driver as db
import gui_register as reg


class GUI_UDI():

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

        self.btns_frame = tk.Frame(self.root)
        self.config_btns_frame()

        self.init_buttons()

        self.btns_frame.pack(padx=20, pady=20, fill='y')

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


    def config_btns_frame(self):
        self.btns_frame.config(bg=color.dark_grey)
        self.btns_frame.columnconfigure(0, weight=1)
        self.btns_frame.columnconfigure(1, weight=1)
        self.btns_frame.columnconfigure(2, weight=1)


    def init_buttons(self):
        self.continue_btn = tk.Button(
            self.btns_frame, 
            text="Siguiente", 
            font=self.gothic_ui_light_14_font,
            bg=color.blue,
            fg=color.white, 
            borderwidth=0,
            command=self.on_continue,
            padx=5,
            pady=5
        )
        self.continue_btn.grid(row=0, column=2, sticky=tk.W+tk.E, padx=20, pady=20)

        self.close_btn = tk.Button(
            self.btns_frame, 
            text="Terminar préstamo", 
            font=self.gothic_ui_light_14_font,
            bg=color.aqua,
            fg=color.white, 
            borderwidth=0,
            command=self.on_close,
            padx=5,
            pady=5
        )
        self.close_btn.grid(row=0, column=1, sticky=tk.W+tk.E, padx=20, pady=20)

        self.register_btn = tk.Button(
            self.btns_frame, 
            text="Registrar nuevo usuari@", 
            font=self.gothic_ui_light_14_font,
            bg=color.aqua,
            fg=color.white, 
            borderwidth=0,
            command=self.on_register,
            padx=5,
            pady=5
        )
        self.register_btn.grid(row=0, column=0, sticky=tk.W+tk.E, padx=20, pady=20)


    def init_string_vars(self):
        self.service_var = tk.StringVar()
        self.service_var.set("Escoja una opción")
        self.service_var.trace("w", self.on_dropdown_changed)
        self.srv_var_flag = True

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
        if self.validate_entries() == False:
            messagebox.showerror(title="Datos incompletos", message="Complete los datos del formulario.")
            return
        
        _usr_id = get_data_from_qr()

        if _usr_id == "Nothing to show":
            messagebox.showerror(title="Error al leer QR", message="No se proporcionó un código QR.")
            return
            
        _srv_id = self.services_dict[self.service_var.get()]
        _obj_id = "-1"
        if self.service_var.get() != "Préstamo de computadora":
            _obj_id = self.rmt_ctrls_dict[self.classroom_control_var.get()] if self.service_var.get() == "Préstamo de control remoto" else extract_number(self.projector_number_var.get())
        
        _res = self.driver.start_loan(_usr_id, _srv_id, _obj_id)

        if _res != "OK":
            messagebox.showerror(title="Error al insertar préstamo", message=_res)
            return
        
        messagebox.showinfo(title="Préstamo exitoso.", message="¡Listo! ;)")
        self.destroy_frame_grid()
        self.init_dropdowns()
            


    def validate_entries(self):
        serv = self.service_var.get()

        if serv == "Escoja una opción":
            return False
        elif serv == "Préstamo de proyector":
            if self.projector_number_var.get() == "Escoja una opción":
                return False
        elif serv == "Préstamo de control remoto":
            if self.classroom_control_var.get() == "Escoja una opción":
                return False
            
        return True


    def on_register(self):
        reg.register_GUI()


    def on_close(self):
        _usr_id = get_data_from_qr()

        if _usr_id == "Nothing to show":
            messagebox.showerror(title="Error al leer QR", message="No se proporcionó un código QR.")
            return
        
        _res = self.driver.close_loan(_usr_id)

        if _res != "OK":
            messagebox.showerror(title="Error al cerrar préstamo", message=_res)
            return
        
        messagebox.showinfo(title="Préstamo concluido.", message="¡Listo! ;)")
        self.destroy_frame_grid()
        self.init_dropdowns()
        

    def on_dropdown_changed(self, *args):
        if self.srv_var_flag == False:
            self.srv_var_flag = True
            return
        
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


    def destroy_frame_grid(self):
        self.service_label.destroy()
        self.service_dropdown.destroy()
        self.control_label.destroy()
        self.classroom_control_dropdown.destroy()
        self.projector_label.destroy()
        self.projector_number_dropdown.destroy()

        self.srv_var_flag = False
        self.service_var.set("Escoja una opción")
        self.classroom_control_var.set("Escoja una opción")
        self.projector_number_var.set("Escoja una opción")


GUI_UDI()