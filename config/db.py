from MySQLdb import _mysql
db=_mysql.connect("localhost", "root", "", "chat")
db.query("""SELECT * FROM user""")
r=db.store_result()

def get_user(email, password):
    db.query("""SELECT * FROM user WHERE email='{}' AND password='{}'""".format(email, password))
    r = db.store_result()
    return r.fetch_row()
