from MySQLdb import _mysql
db=_mysql.connect("localhost", "root", "", "chat")
db.query("""SELECT * FROM user""")
r=db.store_result()

def get_user(email, password):
    db.query("""SELECT * FROM user WHERE email='{}' AND password='{}'""".format(email, password))
    r = db.store_result()
    return r.num_rows()

def create_user(email,password):
    db.query("""INSERT INTO user (email, password) VALUES ('{}', '{}')""".format(email, password))
    db.commit()
    return db.affected_rows()