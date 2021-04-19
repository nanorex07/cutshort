import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class DBManager:

    def connect(self):
        self.conn = sqlite3.connect('db.sqlite3')
        self.curr = self.conn.cursor()

    def close(self):
        self.curr.close()
        self.conn.close()

    def add_user(self, fullname, email, password):
        self.connect()
        query = f"insert into users(fullname, email, password) values('{fullname}','{email}','{generate_password_hash(password,method='sha256')}')"
        self.curr.execute(query)
        self.conn.commit()
        self.close()

    def code_exists(self, code):
        self.connect()
        query = f"select * from urls where code='{code}'"
        self.curr.execute(query)
        res = self.curr.fetchall()
        self.conn.commit()
        self.close()
        if len(res) > 0:
            return True 
        return False

    def find_url(self, code):
        self.connect()
        query = f"select * from urls where code='{code}'"
        self.curr.execute(query)
        res = self.curr.fetchall()
        self.conn.commit()
        self.close()
        return res

    def inc_clicks(self, id):
        self.connect()
        query = f"update urls set clicks=clicks+1 where id={id}"
        self.curr.execute(query)
        self.conn.commit()
        self.close()

    def add_url(self, url, code, user_id):
        self.connect()
        query = f"insert into urls(url, code, user_id, clicks) values('{url}','{code}',{user_id},{0})"
        self.curr.execute(query)
        self.conn.commit()
        self.close()

    def get_exisiting_url(self, url):
        self.connect()
        query = f"select * from urls where url='{url}'"
        self.curr.execute(query)
        r = self.curr.fetchall()
        self.close()
        return r

    def delete_url(self, code):
        self.connect()
        query = f"delete from urls where code='{code}'"
        self.curr.execute(query)
        self.conn.commit()
        self.close()


    def get_urls(self,user_id):
        self.connect()
        query = f"select * from urls where user_id={user_id}"
        self.curr.execute(query)
        res = self.curr.fetchall()
        self.close()
        return res

    def get_user_byid(self,id):
        self.connect()
        query = f"select * from users where id={id}"
        self.curr.execute(query)
        results = self.curr.fetchall()
        self.close()
        return results[0]

    

    def get_user(self, email):
        self.connect()
        query = f"select * from users where email='{email}'"
        self.curr.execute(query)
        results = self.curr.fetchall()
        self.close()
        return results

    def check_password(self, user, password):
        if check_password_hash(user[0][3], password):
            return True
        else:
            return False

