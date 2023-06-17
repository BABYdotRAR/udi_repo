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
        self.cursor.execute("SELECT * FROM tc_remote_controls")
        rmt_ctrls = [(rmtctrl_classroom, rmtctrl_id) for rmtctrl_id, rmtctrl_classroom in self.cursor]
        return rmt_ctrls
    

    def get_projectors(self):
        self.cursor.execute("SELECT prjtr_id FROM tc_projectors")
        projectors = [prjtr_id for prjtr_id in self.cursor]
        return projectors
    
    
    def create_new_user(self, params):
        usr_id = params["id"]
        usr_name = params["name"]
        usr_last_name = params["lastname"]
        usr_phone_number = params["phone"]

        try:
            self.cursor.execute("INSERT INTO te_users VALUES (?,?,?,?)", 
                                (usr_id, usr_name, usr_last_name, usr_phone_number))
        except mariadb.Error as e:
            return f"Error: {e}"
        
        return "OK"
    

    def close_connection(self):
        self.conn.close()
