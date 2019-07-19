import sqlite3, datetime

class Database(object):
    """Create Database"""
    def __init__(self):
        self.conn = sqlite3.connect('dyeing.db')
        self.cursor = self.conn.cursor()
    
        self.cursor.execute("CREATE TABLE IF NOT EXISTS transition(id INTEGER PRIMARY KEY, machine INTEGER, s_time TEXT, r_time TEXT, r_status TEXT, t_date TEXT)")
    
    def insert_value(self, machine, s_time, r_time, r_status, t_date):
        self.cursor.execute("INSERT INTO transition(machine, s_time, r_time, r_status, t_date) VALUES(?,?,?,?,?)",(machine, s_time, r_time, r_status, t_date))
        self.conn.commit()
    
    def fetch_latest(self):
        try:
            latest = self.cursor.execute("SELECT * FROM transition ORDER BY id DESC LIMIT 1")
        except:
            pass
        return latest
    
    def update_value(self, r_status):
        r_time = datetime.datetime.now().strftime("%H:%M:%S")
        # Find the latest data
        m = self.cursor.execute("SELECT id FROM transition ORDER BY id DESC LIMIT 1").fetchall()[0][0]
        print(m)

        id = m

        print(id)
        
        self.cursor.execute("UPDATE transition SET r_time=?, r_status=? WHERE id=?", (r_time, r_status, id))

        self.conn.commit()
    
    def fetch_today(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("SELECT * FROM transition WHERE t_date=?",(today,))

        query = self.cursor.fetchall()

        return query
    
    def delete_entity(self, n=1):
        self.cursor.execute('DELETE FROM transition order by id desc limit {}'.format(n))

        self.conn.commit()
    
    def delete_all(self):
        self.cursor.execute("DELETE FROM transition")

        self.conn.commit()
    
    def db_close(self):
        self.cursor.close()
        self.conn.close()
