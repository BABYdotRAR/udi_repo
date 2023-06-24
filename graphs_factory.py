import matplotlib as mp
import matplotlib.pyplot as plt
import db_driver as db
import numpy as np

from date_time_handler import get_current_day_name

class Graph_Factory:
    def __init__(self):
        self.driver = db.DB_Driver()
        self.week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


    def show_week_bar_graph(self):
        computer_loans = [self.driver.get_loans_by_day_in_current_week(day, 1) for day in self.week_days]
        projector_loans = [self.driver.get_loans_by_day_in_current_week(day, 2) for day in self.week_days]
        remote_control_loans = [self.driver.get_loans_by_day_in_current_week(day, 3) for day in self.week_days]

        x_indexes = np.arange(len(self.week_days))
        bar_width = 0.25
        plt.bar(x_indexes - bar_width, computer_loans, width=bar_width, label= "Computadoras")
        plt.bar(x_indexes, projector_loans, width=bar_width, label= "Proyectores")
        plt.bar(x_indexes + bar_width, remote_control_loans, width=bar_width, label= "Controles")
        plt.xticks(ticks=x_indexes, labels=self.week_days)
        plt.legend()

        plt.title("Estadísticas de préstamo durante la presente semana")
        plt.xlabel("Día de la semana")
        plt.ylabel("Total de préstamos")
        plt.show()


    def show_daily_bar_graph(self):
        computer_loans = [self.driver.get_loans_by_day_in_current_week(get_current_day_name(), 1)]
        projector_loans = [self.driver.get_loans_by_day_in_current_week(get_current_day_name(), 2)]
        remote_control_loans = [self.driver.get_loans_by_day_in_current_week(get_current_day_name(), 3)]

        x_indexes = np.arange(1)
        bar_width = 0.25
        plt.bar(x_indexes - bar_width, computer_loans, width=bar_width, label= "Computadoras")
        plt.bar(x_indexes, projector_loans, width=bar_width, label= "Proyectores")
        plt.bar(x_indexes + bar_width, remote_control_loans, width=bar_width, label= "Controles")
        plt.xticks(ticks=x_indexes, labels=[get_current_day_name()])
        plt.legend()

        plt.title("Estadísticas de préstamo durante la presente semana")
        plt.xlabel("Día de la semana")
        plt.ylabel("Total de préstamos")
        plt.show()
