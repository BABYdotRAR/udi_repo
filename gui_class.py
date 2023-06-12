import tkinter as tk

class GUI_UDI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("UDI ESIT")
        self.root.geometry("800x600")

        self.welcome_label = tk.Label(
            self.root,
            text="Bienvenido de nuevo, por favor selecciona una opción",
            font=('Yu Gothic UI Light', 14)
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
        self.service_dropdown.config(font=('Yu Gothic UI Light', 14))
        self.service_dropdown.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.control_label = tk.Label(
            self.form_frame,
            text="Seleccione el control a prestar:",
            font=('Yu Gothic UI Light', 14)
        )
        self.classroom_control_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.classroom_control_var, 
            "102", 
            "E-202", 
            "Lab 2"
        )
        self.classroom_control_dropdown.config(font=('Yu Gothic UI Light', 14))

        self.projector_label = tk.Label(
            self.form_frame,
            text="Seleccione el número de cañón a prestar:",
            font=('Yu Gothic UI Light', 14)
        )
        self.projector_number_dropdown = tk.OptionMenu(
            self.form_frame, 
            self.projector_number_var, 
            "1", 
            "2", 
            "3"
        )
        self.projector_number_dropdown.config(font=('Yu Gothic UI Light', 14))

        self.form_frame.pack(padx=10, pady=10)

        self.continue_btn = tk.Button(
            self.root, 
            text="Siguiente", 
            font=('Yu Gothic UI Light', 14),
            command=self.on_continue
        )
        self.continue_btn.pack(padx=20, pady=20)

        self.root.mainloop()

    def init_string_vars(self):
        self.service_var = tk.StringVar()
        self.service_var.trace("w", self.on_dropdown_changed)

        self.classroom_control_var = tk.StringVar()
        self.projector_number_var = tk.StringVar()

    def on_continue(self):
        print(self.service_var.get())
        print(self.classroom_control_var.get())
        print(self.projector_number_var.get())

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

