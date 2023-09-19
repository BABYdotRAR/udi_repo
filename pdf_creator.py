from fpdf import FPDF

import env_variables as env
import date_time_handler as dth
from db_driver import DB_Driver
from graphs_factory import Graph_Factory

esit_logo_path = env.PROJECT_PATH + "\\img\\ESIT.png"
months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
db = DB_Driver()
gf = Graph_Factory()

def create(month):
    month_interval = dth.get_month(month)
    start, end = month_interval[0], month_interval[1]
    computer_loans = db.get_total_loans_by_service_between(start, end, 1)
    projector_loans = db.get_total_loans_by_service_between(start, end, 2)
    remote_controls_loans = db.get_total_loans_by_service_between(start, end, 3)
    total_loans = db.get_total_loans_between(start, end)

    gf.create_loans_between_bar_graph(start, end, "{}_2023.png".format(months[month - 1]))
    img_path = env.PROJECT_PATH + "\\{}_2023.png".format(months[month - 1])
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_font('Arial', 'B', 16)
    pdf.add_page()

    pdf.cell(0, 5, "Reporte mensual: {}".format(months[month - 1]), 0, 1, 'C')
    pdf.cell(0, 5, r"Sistema de control UDI", 0, 1, 'C')
    pdf.cell(40, 5, "", 0, 1)

    pdf.set_font('Arial', '', 10)

    pdf.image(esit_logo_path, 150, 30, 30)
    pdf.cell(100, 5, r"Total de préstamos en el mes: ", 0, 0)
    pdf.cell(40, 5, str(total_loans), 0, 1)
    pdf.cell(100, 5, r"Total de préstamos de computadora en el mes: ", 0, 0)
    pdf.cell(40, 5, str(computer_loans), 0, 1)
    pdf.cell(100, 5, r"Total de préstamos de proyector en el mes: ", 0, 0)
    pdf.cell(40, 5, str(projector_loans), 0, 1)
    pdf.cell(100, 5, r"Total de préstamos de control en el mes: ", 0, 0)
    pdf.cell(40, 5, str(remote_controls_loans), 0, 1)
    pdf.image(img_path, None, None, 100)
    pdf.output("{}_2023.pdf".format(months[month - 1]), "F")


create(6)