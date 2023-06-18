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


    def close_connection(self):
        self.conn.close()
