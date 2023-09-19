import mariadb
import sys
import env_variables as env

from string_validator import extract_number
from date_time_handler import get_start_of_week_datetime


class DB_Driver:
    def __init__(self):
        self.init_connection()
        self.cursor = self.conn.cursor()


    def init_connection(self):
        try:
            self.conn = mariadb.connect(
                user=env.DATABASE_USER,
                password=env.DATABASE_PASSWORD,
                host="localhost",
                port=3306,
                database=env.DATABASE_NAME
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    
    def get_available_remote_controls(self):
        query = """SELECT rmtctrl_id, rmtctrl_classroom 
        FROM tc_remote_controls WHERE is_Available = TRUE"""
        self.conn.commit()
        self.cursor.execute(query)
        rmt_ctrls = [(rmtctrl_classroom, rmtctrl_id) for rmtctrl_id, rmtctrl_classroom in self.cursor]
        return rmt_ctrls
    

    def get_available_projectors(self):
        query = 'SELECT prjtr_id FROM tc_projectors WHERE is_Available = TRUE'
        self.conn.commit()
        self.cursor.execute(query)
        projectors = [prjtr_id for prjtr_id in self.cursor]
        return projectors
    

    def create_new_user(self, params):
        usr_id = params["id"]
        usr_name = params["name"]
        usr_last_name = params["lastname"]
        last_col_value = params["last_col"]
        contact_option = params["option"]

        last_col = 'usr_phone_number' if contact_option == "phone" else 'usr_email'

        try:
            partial_query = "INSERT INTO te_users (usr_id, usr_name, usr_last_name, "
            self.cursor.execute(partial_query + last_col + ") VALUES (?,?,?,?)", 
                                (usr_id, usr_name, usr_last_name, last_col_value))
        except mariadb.Error as e:
            return f"Error: {e}"
        
        self.conn.commit()
        return "OK"
    

    def get_email_by_user_id(self, user_id):
        self.conn.commit()
        query = "SELECT usr_email FROM te_users WHERE usr_id = ?"
        try:
            self.cursor.execute(query, (user_id,))
        except mariadb.Error as e:
            return f"Error: {e}"
        if self.cursor.rowcount == 0:
            return "Error: Boleta no válida"
        return self.cursor.fetchone()[0]


    def update_email_by_user_id(self, user_id, new_email):
        self.conn.commit()
        query = "UPDATE te_users SET usr_email = ? WHERE usr_id = ?"
        try:
            self.cursor.execute(query, (new_email, user_id))
        except mariadb.Error as e:
            return f"Error: {e}"
        self.conn.commit()
        return "OK"
        

    def update_projector_status(self, projector_id, new_status):
        self.conn.commit()
        query = "UPDATE tc_projectors SET is_available = ? WHERE prjtr_id = ?"
        try:
            self.cursor.execute(query, (new_status, projector_id))
        except mariadb.Error as e:
            return f"Error: {e}"
        self.conn.commit()
        return "OK"


    def update_remote_control_status(self, rmtctrl_id, new_status):
        self.conn.commit()
        query = "UPDATE tc_remote_controls SET is_available = ? WHERE rmtctrl_id = ?"
        try:
            self.cursor.execute(query, (new_status, rmtctrl_id))
        except mariadb.Error as e:
            return f"Error: {e}"
        self.conn.commit()
        return "OK"

    def insert_remote_control(self, classroom):
        self.conn.commit()
        query = "INSERT INTO tc_remote_controls(rmtctrl_classroom, is_available) VALUES ('?', True)"
        try:
            self.cursor.execute(query, (classroom, ))
        except mariadb.Error as e:
            return f"Error: {e}"
        self.conn.commit()
        return "OK"
    
    
    def insert_projector(self, prjtr_branch):
        self.conn.commit()
        query = "INSERT INTO tc_projectors(prjtr_branch, is_available) VALUES ('?', True)"
        try:
            self.cursor.execute(query, (prjtr_branch, ))
        except mariadb.Error as e:
            return f"Error: {e}"
        self.conn.commit()
        return "OK"
    

    def start_loan(self, id_usr, id_srv, id_obj):
        try:
            self.cursor.execute("CALL insert_loan(?,?,?,@v)", (id_usr, id_srv, id_obj))
        except mariadb.Error as e:
            return f"Error: {e}"
        
        self.conn.commit()
        self.cursor.execute("SELECT @v")
        _res = 1
        for v in self.cursor:
            _res = extract_number(str(v))

        if _res == 0:
            return "OK"
        else:
            return "Error: boleta inválida, por favor regístrese primero"
    

    def close_loan(self, id_usr):
        try:
            self.cursor.execute("CALL close_loan(?, @v)", (id_usr,))
        except mariadb.Error as e:
            return f"Error: {e}"
        
        self.conn.commit()
        self.cursor.execute("SELECT @v")
        _res = 1
        for v in self.cursor:
            _res = extract_number(str(v))

        if _res == 0:
            return "OK"
        else:
            return "Error: boleta inválida, por favor regístrese primero"


    def get_current_loaned_controls(self):
        self.conn.commit()
        query = """SELECT a.usr_id, c.rmtctrl_classroom FROM te_loans a 
        INNER JOIN te_loan_complement b ON a.cmplmt_id = b. cmplmt_id 
        INNER JOIN tc_remote_controls c ON b.rmtctrl_id = c.rmtctrl_id 
        WHERE a.is_active = TRUE"""
        self.cursor.execute(query)
        rmt_ctrls_loaned = [(usr_id, rmtctrl_classroom) for usr_id, rmtctrl_classroom in self.cursor]
        return rmt_ctrls_loaned


    def get_current_loaned_projectors(self):
        self.conn.commit()
        query = """SELECT a.usr_id, c.prjtr_id FROM te_loans a 
        INNER JOIN te_loan_complement b ON a.cmplmt_id = b. cmplmt_id 
        INNER JOIN tc_projectors c ON b.prjtr_id = c.prjtr_id 
        WHERE a.is_active = TRUE"""
        self.cursor.execute(query)
        projectors_loaned = [(usr_id, prjtr_id) for usr_id, prjtr_id in self.cursor]
        return projectors_loaned


    def get_current_users_in_computer_loan(self):
        self.conn.commit()
        query = "SELECT usr_id FROM te_loans WHERE cmplmt_id IS NULL AND is_active = TRUE"
        self.cursor.execute(query)
        users_in_loan = [usr_id for usr_id in self.cursor]
        return users_in_loan
    

    def get_loans_by_day_in_current_week(self, day_name, loan_type):
        self.conn.commit()
        week_start = get_start_of_week_datetime()
        query = f'SELECT COUNT(*) FROM te_loans WHERE start_at > "{week_start}" AND day_name = ? AND service_id = ?'
        try:
            self.cursor.execute(query, (day_name, loan_type))
        except mariadb.Error as e:
            return f"Error: {e}"
        return self.cursor.fetchone()[0]
    

    def get_loans_by_service_between(self, start_at, end_at, service_id) -> dict:
        query = f'CALL get_total_loans_between(?,?,?)'
        try:
            self.cursor.execute(query, (start_at, end_at, service_id))
        except mariadb.Error as e:
            return f"Error: {e}"
        fetched = self.cursor.fetchall()
        return dict((row[0], row[1]) for row in fetched)


    def get_total_loans_between(self, start_at, end_at):
        query = """SELECT  COUNT(*) FROM  te_loans WHERE start_at BETWEEN '{}' AND '{}';""".format(start_at, end_at)
        try:
            self.cursor.execute(query)
        except mariadb.Error as e:
            return f"Error: {e}"
        return self.cursor.fetchone()[0]
    
    def get_total_loans_by_service_between(self, start_at, end_at, service): 
        query = """SELECT  COUNT(*) FROM  te_loans WHERE service_id = {} AND start_at BETWEEN '{}' AND '{}';""".format(service, start_at, end_at)
        try:
            self.cursor.execute(query)
        except mariadb.Error as e:
            return f"Error: {e}"
        return self.cursor.fetchone()[0]

    def close_connection(self):
        self.conn.close()
