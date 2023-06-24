import tkinter as tk
from tkinter import font
from tkinter import messagebox

from qr_reader import get_data_from_qr
from string_validator import extract_number
import colors as color
import db_driver as db
import gui_register as reg
import gui_loans_list as loans
import graphs_factory as factory
import gui_resend_qr as resend
import gui_issue as report


class GUI_UDI():
    def __init__(self):
        self.root = tk.Tk()
        
        self.config_menubar()
        self.config_root()
        self.driver = db.DB_Driver()
        self.graphs = factory.Graph_Factory()
        self.init_fonts()
        self.init_string_vars()

        self.welcome_label = self.create_label(self.root, "Bienvenido de nuevo, por favor selecciona una opción", self.gothic_ui_bold_16_font)
        self.welcome_label.pack(padx=10, pady=10)

        self.form_frame = self.create_frame(self.root, background_color=color.blue_ocean)
        self.init_dropdowns()
        self.form_frame.pack(padx=10, pady=10, fill='both')

        self.btns_frame = self.create_frame(self.root, total_cols=4, background_color=color.blue_ocean)
        self.init_buttons()
        self.btns_frame.pack(padx=10, pady=10, fill='x')

        self.manual_reg_frame = self.create_frame(self.root, background_color=color.blue_ocean)
        self.init_manual_reg_widgets()
        self.manual_reg_frame.pack(padx=10, pady=10, fill='x')

        self.credits_label = self.create_label(self.root, "© 2023 Oscar López All rights Reserved",self.gothic_ui_light_10_font)
        self.credits_label.pack(padx=10, pady=10, side="bottom")

        self.root.state('zoomed')
        self.root.mainloop()


    def config_root(self):
        self.root.title("UDI ESIT")
        self.root.geometry("800x600")
        self.root.config(bg=color.dark_blue, menu=self.menubar)


    def config_menubar(self):
        self.menubar = tk.Menu(self.root)
        self.user_menu = tk.Menu(self.menubar, tearoff=False)
        self.dev_menu = tk.Menu(self.menubar, tearoff=False)
        self.report_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Reporte", menu=self.report_menu)
        self.menubar.add_cascade(label="Usuario", menu=self.user_menu)
        self.menubar.add_cascade(label="Ayuda", menu=self.dev_menu)
        self.user_menu.add_command(label="Reenviar QR", command=self.on_resend_qr)
        self.report_menu.add_command(label="Ver estadísticas de hoy", command=self.on_show_current_daily_stats)
        self.report_menu.add_command(label="Ver estadísticas semanales", command=self.on_show_current_week_stats)
        self.report_menu.add_separator()
        self.report_menu.add_command(label="Reporte semanal", command=self.command_test)
        self.report_menu.add_command(label="Reporte mensual", command=self.command_test)
        self.dev_menu.add_command(label="Reportar un problema con la aplicación", command=self.on_report)


    def command_test(self):
        messagebox.showinfo(title="En desarrollo", message="No disponible por el momento.\nEsta función se encuentra en desarrollo.")


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
    

    def init_fonts(self):
        self.gothic_ui_light_10_font = font.Font(family='Yu Gothic UI Light', size=10)
        self.gothic_ui_light_12_font = font.Font(family='Yu Gothic UI Light', size=12)
        self.gothic_ui_light_14_font = font.Font(family='Yu Gothic UI Light', size=14)
        self.gothic_ui_bold_14_font = font.Font(family='Yu Gothic UI bold', size=14)
        self.gothic_ui_bold_16_font = font.Font(family='Yu Gothic UI bold', size=16)


    def init_buttons(self):
        self.continue_btn = self.create_button(self.form_frame, self.on_continue, "Siguiente", self.gothic_ui_light_14_font)
        self.continue_btn.grid(row=3, column=2, sticky=tk.W+tk.E, padx=20, pady=20)

        self.close_btn = self.create_button(self.btns_frame, self.on_close, "Terminar préstamo", self.gothic_ui_light_14_font, text_color=color.white, background_color=color.aqua)
        self.close_btn.grid(row=1, column=1, sticky=tk.W+tk.E, padx=20, pady=20)

        self.register_btn = self.create_button(self.btns_frame, self.on_register, "Registrar nuevo usuari@", self.gothic_ui_light_14_font, text_color=color.white, background_color=color.aqua)
        self.register_btn.grid(row=1, column=0, sticky=tk.W+tk.E, padx=20, pady=20)

        self.current_loans_btn = self.create_button(self.btns_frame, self.on_current_loans, "Ver préstamos activos", self.gothic_ui_light_14_font, text_color=color.white, background_color=color.blue)
        self.current_loans_btn.grid(row=1, column=2, sticky=tk.W+tk.E, padx=20, pady=20)

        self.refresh_btn = self.create_button(self.btns_frame, self.on_refresh, "Refrescar", self.gothic_ui_light_14_font, text_color=color.white, background_color=color.blue)
        self.refresh_btn.grid(row=1, column=3, sticky=tk.W+tk.E, padx=20, pady=20)


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
        self.services_dict = {"Préstamo de computadora":1, "Préstamo de proyector":2, "Préstamo de control remoto":3}
        self.rmt_ctrls_list = self.driver.get_available_remote_controls()
        self.rmt_ctrls_dict = dict(self.rmt_ctrls_list)
        self.projectors = self.driver.get_available_projectors()

        self.service_label = self.create_label(self.form_frame, "Seleccione el servicio solicitado:",self.gothic_ui_light_14_font,background_color=color.blue_ocean)
        self.service_label.grid(row=0, column=0, sticky=tk.W+tk.E, padx=10, pady=10)
        self.service_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.service_var, 
            *self.services_dict.keys()
        )
        self.service_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.light_purple, fg=color.black, borderwidth=0)
        self.service_dropdown.grid(row=1, column=0, sticky=tk.W+tk.E, padx=10, pady=10)

        self.control_label = self.create_label(self.form_frame, "Seleccione el control a prestar:",self.gothic_ui_light_14_font,background_color=color.blue_ocean)
        self.classroom_control_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.classroom_control_var, 
            *self.rmt_ctrls_dict.keys()
        )
        self.classroom_control_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.light_purple, fg=color.black, borderwidth=0)

        self.projector_label = self.create_label(self.form_frame, "Seleccione el número de cañón a prestar:",self.gothic_ui_light_14_font,background_color=color.blue_ocean)
        self.projector_number_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.projector_number_var, 
            *self.projectors
        )
        self.projector_number_dropdown.config(font=self.gothic_ui_light_14_font, bg=color.light_purple, fg=color.black, borderwidth=0)


    def init_manual_reg_widgets(self):
        self.manual_reg_flag = False

        self.user_id_label = self.create_label(self.manual_reg_frame, "Ingrese la boleta:", self.gothic_ui_light_14_font, background_color=color.blue_ocean)

        self.user_id_entry = tk.Entry(
            self.manual_reg_frame,
            textvariable=self.user_id_var,
            font=self.gothic_ui_light_14_font
        )
        
        self.manual_register_btn = self.create_button(self.manual_reg_frame, self.on_manual_continue, "Siguiente", self.gothic_ui_light_14_font)


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
        loans.GUI_Current_Loans()


    def on_refresh(self):
        self.destroy_frame_grid()
        self.init_dropdowns()
        

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


    def on_show_current_week_stats(self):
        self.graphs.show_week_bar_graph()


    def on_show_current_daily_stats(self):
        self.graphs.show_daily_bar_graph()


    def on_resend_qr(self):
        resend.GUI_Resend_QR()


    def on_report(self):
        report.GUI_Issue()

        
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