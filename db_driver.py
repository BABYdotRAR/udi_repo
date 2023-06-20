import mariadb
import sys
import env_variables as env


class DB_Driver:
    def __init__(self):
        self.init_connection()
        print("Connection ")
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

    
    def get_remote_controls(self):
        self.cursor.execute("SELECT rmtctrl_id, rmtctrl_classroom FROM tc_remote_controls WHERE is_Available = TRUE")
        rmt_ctrls = [(rmtctrl_classroom, rmtctrl_id) for rmtctrl_id, rmtctrl_classroom in self.cursor]
        return rmt_ctrls
    

    def get_projectors(self):
        self.cursor.execute("SELECT prjtr_id FROM tc_projectors WHERE is_Available = TRUE")
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
            self.cursor.execute("INSERT INTO te_users (usr_id, usr_name, usr_last_name, " 
                                + last_col + ") VALUES (?,?,?,?)", 
                                (usr_id, usr_name, usr_last_name, last_col_value))
        except mariadb.Error as e:
            return f"Error: {e}"
        
        self.conn.commit()
        return "OK"
    

    def start_loan(self, id_usr, id_srv, id_obj):
        try:
            self.cursor.execute("CALL insert_loan(?,?,?)", (id_usr, id_srv, id_obj))
        except mariadb.Error as e:
            return f"Error: {e}"
        
        self.conn.commit()
        return "OK"
    

    def close_loan(self, id_usr):
        try:
            self.cursor.execute("CALL close_loan(?)", (id_usr,))
        except mariadb.Error as e:
            return f"Error: {e}"
        
        self.conn.commit()
        return "OK"


    def get_current_loaned_controls(self):
        query = "select a.usr_id, c.rmtctrl_classroom from te_loans a inner join te_loan_complement b on a.cmplmt_id = b. cmplmt_id inner join tc_remote_controls c on b.rmtctrl_id = c.rmtctrl_id WHERE a.is_active = TRUE"
        self.cursor.execute(query)
        rmt_ctrls_loaned = [(usr_id, rmtctrl_classroom) for usr_id, rmtctrl_classroom in self.cursor]
        return rmt_ctrls_loaned


    def get_current_loaned_projectors(self):
        query = "select a.usr_id, c.prjtr_id from te_loans a inner join te_loan_complement b on a.cmplmt_id = b. cmplmt_id inner join tc_projectors c on b.prjtr_id = c.prjtr_id WHERE a.is_active = TRUE"
        self.cursor.execute(query)
        projectors_loaned = [(usr_id, prjtr_id) for usr_id, prjtr_id in self.cursor]
        return projectors_loaned

    def get_current_loaned_computers(self):
        query = "select usr_id from te_loans WHERE cmplmt_id IS NULL AND is_active = TRUE"
        self.cursor.execute(query)
        projectors_loaned = [usr_id for usr_id in self.cursor]
        return projectors_loaned
    

    def close_connection(self):
        self.conn.close()
