import tkinter as tk
from tkinter import font
from tkinter import messagebox

from qr_reader import get_data_from_qr
from string_validator import extract_number
import colors as color
import db_driver as db
import gui_register as reg
import gui_loans_list as loans


class GUI_UDI():

    def __init__(self):
        self.root = tk.Tk()

        self.config_root()
        self.driver = db.DB_Driver()

        self.gothic_ui_light_14_font = font.Font(family='Yu Gothic UI Light', size=14)
        self.gothic_ui_light_10_font = font.Font(family='Yu Gothic UI Light', size=10)
        self.gothic_ui_16_font = font.Font(family='Yu Gothic UI bold', size=16)

        self.welcome_label = tk.Label(
            self.root,
            text="Bienvenido de nuevo, por favor selecciona una opción",
            font=self.gothic_ui_16_font,
            fg=color.white,
            bg=color.dark_blue
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

        self.btns_frame.pack(padx=10, pady=10, fill='y')

        self.manual_reg_frame = tk.Frame(self.root)
        self.config_manual_reg_frame()

        self.init_manual_reg_widgets()

        self.manual_reg_frame.pack(padx=10, pady=10, fill='x')

        self.credits_label = tk.Label(
            self.root,
            text="© 2023 Oscar López All rights Reserved",
            font=self.gothic_ui_light_10_font,
            fg=color.white,
            bg=color.dark_blue
        )
        self.credits_label.pack(padx=10, pady=10, side="bottom")

        self.root.state('zoomed')
        self.root.mainloop()


    def config_root(self):
        self.root.title("UDI ESIT")
        self.root.geometry("800x600")
        self.root.config(bg=color.dark_blue)


    def config_form_frame(self):
        self.form_frame.config(bg=color.blue_ocean)
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=1)
        self.form_frame.columnconfigure(2, weight=1)


    def config_btns_frame(self):
        self.btns_frame.config(bg=color.blue_ocean)
        self.btns_frame.columnconfigure(0, weight=1)
        self.btns_frame.columnconfigure(1, weight=1)
        self.btns_frame.columnconfigure(2, weight=1)


    def config_manual_reg_frame(self):
        self.manual_reg_frame.config(bg=color.blue_ocean)
        self.manual_reg_frame.columnconfigure(0, weight=1)
        self.manual_reg_frame.columnconfigure(1, weight=1)
        self.manual_reg_frame.columnconfigure(2, weight=1)


    def init_buttons(self):
        self.continue_btn = tk.Button(
            self.btns_frame, 
            text="Siguiente", 
            font=self.gothic_ui_light_14_font,
            bg=color.light_purple,
            fg=color.black, 
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

        self.current_loans_btn = tk.Button(
            self.btns_frame, 
            text="Ver préstamos activos", 
            font=self.gothic_ui_light_14_font,
            bg=color.blue,
            fg=color.white, 
            borderwidth=0,
            command=self.on_current_loans,
            padx=5,
            pady=5
        )
        self.current_loans_btn.grid(row=1, column=1, sticky=tk.W+tk.E, padx=20, pady=20)


    def init_string_vars(self):
        self.service_var = tk.StringVar()
        self.service_var.set("Escoja una opción")
        self.service_var.trace("w", self.on_dropdown_changed)
        self.srv_var_flag = True

        self.classroom_control_var = tk.StringVar()
        self.classroom_control_var.set("Escoja una opción")
        self.projector_number_var = tk.StringVar()
        self.projector_number_var.set("Escoja una opción")
        self.user_id_var = tk.StringVar()


    def init_dropdowns(self):
        self.service_label = tk.Label(
            self.form_frame,
            text="Seleccione el servicio solicitado:",
            font=self.gothic_ui_light_14_font,
            fg=color.white,
            bg=color.blue_ocean
        )
        self.service_label.grid(row=0, column=0, sticky=tk.W+tk.E, padx=10, pady=10)
        self.services_dict = {"Préstamo de computadora":1, "Préstamo de proyector":2, "Préstamo de control remoto":3}
        self.service_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.service_var, 
            *self.services_dict.keys()
        )
        self.service_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.light_purple, fg=color.black, borderwidth=0)
        self.service_dropdown.grid(row=1, column=0, sticky=tk.W+tk.E, padx=10, pady=10)

        self.control_label = tk.Label(
            self.form_frame,
            text="Seleccione el control a prestar:",
            font=self.gothic_ui_light_14_font,
            fg=color.white,
            bg=color.blue_ocean
        )
        self.rmt_ctrls_list = self.driver.get_remote_controls()
        self.rmt_ctrls_dict = dict(self.rmt_ctrls_list)
        self.classroom_control_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.classroom_control_var, 
            *self.rmt_ctrls_dict.keys()
        )
        self.classroom_control_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.light_purple, fg=color.black, borderwidth=0)

        self.projector_label = tk.Label(
            self.form_frame,
            text="Seleccione el número de cañón a prestar:",
            font=self.gothic_ui_light_14_font,
            fg=color.white,
            bg=color.blue_ocean
        )
        self.projectors = self.driver.get_projectors()
        self.projector_number_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.projector_number_var, 
            *self.projectors
        )
        self.projector_number_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.light_purple, fg=color.black, borderwidth=0)


    def init_manual_reg_widgets(self):
        self.manual_reg_flag = False

        self.user_id_label = tk.Label(
            self.manual_reg_frame,
            text="Ingrese la boleta:",
            font=self.gothic_ui_light_14_font,
            fg=color.white,
            bg=color.blue_ocean
        )
        
        self.user_id_entry = tk.Entry(
            self.manual_reg_frame,
            textvariable=self.user_id_var,
            font=self.gothic_ui_light_14_font
        )
        
        self.manual_register_btn = tk.Button(
            self.manual_reg_frame, 
            text="Siguiente", 
            font=self.gothic_ui_light_14_font,
            bg=color.light_purple,
            fg=color.black, 
            borderwidth=0,
            command=self.on_manual_continue,
            padx=5,
            pady=5
        )


    def on_continue(self):
        if self.manual_reg_flag:
            self.grid_forget_manual_reg_widgets()
        
        if self.validate_entries() == False:
            messagebox.showerror(title="Datos incompletos", message="Complete los datos del formulario.")
            return
        
        _usr_id = get_data_from_qr()

        if _usr_id == "Nothing to show":
            if self.manual_reg_flag == False:
                self.grid_manual_reg_widgets()

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
        
        self.destroy_frame_grid()
        self.init_dropdowns()
        messagebox.showinfo(title="Préstamo exitoso.", message="¡Listo! ;)\nInicia préstamo para: "+_usr_id)           


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
        
        self.destroy_frame_grid()
        self.init_dropdowns()
        messagebox.showinfo(title="Préstamo concluido.", message="¡Listo! ;)\nTermina préstamo para: "+_usr_id)  
      

    def on_current_loans(self):
        loans.GUI_list()


    def on_manual_continue(self):
        if self.validate_entries() == False:
            messagebox.showerror(title="Datos incompletos", message="Complete los datos del formulario.")
            return
        
        _usr_id = self.user_id_var.get()
        _srv_id = self.services_dict[self.service_var.get()]
        _obj_id = "-1"
        if self.service_var.get() != "Préstamo de computadora":
            _obj_id = self.rmt_ctrls_dict[self.classroom_control_var.get()] if self.service_var.get() == "Préstamo de control remoto" else extract_number(self.projector_number_var.get())
        
        _res = self.driver.start_loan(_usr_id, _srv_id, _obj_id)

        if _res != "OK":
            messagebox.showerror(title="Error al insertar préstamo", message=_res)
            return
        
        self.grid_forget_manual_reg_widgets()
        self.destroy_frame_grid()
        self.init_dropdowns()
        messagebox.showinfo(title="Préstamo exitoso.", message="¡Listo! ;)\nInicia préstamo para: "+_usr_id)


    def on_dropdown_changed(self, *args):
        if self.srv_var_flag == False:
            self.srv_var_flag = True
            return
        
        option = self.service_var.get()

        if option == "Préstamo de proyector":
            self.projector_label.grid(row=2, column=1, sticky=tk.W+tk.E, padx=10, pady=10)
            self.projector_number_dropdown.grid(row=2, column=2, sticky=tk.W+tk.E, padx=10, pady=10)

            self.control_label.grid_forget()
            self.classroom_control_dropdown.grid_forget()
        elif option == "Préstamo de control remoto":
            self.control_label.grid(row=2, column=1, sticky=tk.W+tk.E, padx=10, pady=10)
            self.classroom_control_dropdown.grid(row=2, column=2, sticky=tk.W+tk.E, padx=10, pady=10)

            self.projector_label.grid_forget()
            self.projector_number_dropdown.grid_forget()
        else:
            self.control_label.grid_forget()
            self.classroom_control_dropdown.grid_forget()
            self.projector_label.grid_forget()
            self.projector_number_dropdown.grid_forget()


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
        

    def grid_manual_reg_widgets(self):
        self.manual_reg_flag = True

        self.user_id_label.grid(row=0, column=0, sticky=tk.W+tk.E, padx=10, pady=10)
        self.user_id_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=10, pady=10)
        self.manual_register_btn.grid(row=0, column=2, sticky=tk.W+tk.E, padx=10, pady=10)

    
    def grid_forget_manual_reg_widgets(self):
        self.manual_reg_flag = False
        
        self.user_id_label.grid_forget()
        self.user_id_entry.grid_forget()
        self.manual_register_btn.grid_forget()


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