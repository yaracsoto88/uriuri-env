from MySQLdb import _mysql
db=_mysql.connect("localhost", "root", "", "chat")
db.query("""SELECT * FROM user""")
r=db.store_result()

def get_user(email, password):
    db.query("""SELECT * FROM user WHERE email='{}' AND password='{}'""".format(email, password))
    r = db.store_result()
    return r.num_rows()

def create_user(email,username,password):
    db.query("""INSERT INTO user (email, username, password) VALUES ('{}','{}','{}')""".format(email,username, password))

    return db.affected_rows()

# db.query(""" Delete from user where username ="b";""")
# user =  create_user("s","b","c")