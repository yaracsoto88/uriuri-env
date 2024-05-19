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
def get_friends(email):
    db.query("""
    SELECT friend.username 
    FROM user 
    JOIN userfriend ON user.id = userfriend.user_id 
    JOIN user AS friend ON userfriend.friend_id = friend.id
    WHERE user.email = '{}'
    UNION
    SELECT friend.username 
    FROM user 
    JOIN userfriend ON user.id = userfriend.friend_id 
    JOIN user AS friend ON userfriend.user_id = friend.id
    WHERE user.email = '{}'
    """.format(email, email))
    r = db.store_result()
    rows = r.fetch_row(maxrows=0)

    return [row[0].decode('utf-8') for row in rows]

# print ( get_friends("michael@mail.com"))

def get_idfriend(username):
    db.query("""SELECT id FROM user WHERE username = '{}'""".format(username))
    r = db.store_result()
    return r.fetch_row(maxrows=0)[0][0].decode('utf-8')


def get_idfriend_by_mail(email):
    db.query("""SELECT id FROM user WHERE email = '{}'""".format(email))
    r = db.store_result()
    return r.fetch_row(maxrows=0)[0][0].decode('utf-8')

def get_messages(email_user, idfriend):
    id_user= get_idfriend_by_mail(email_user)
    db.query("""
    SELECT sender_id, message 
    FROM message
    WHERE (sender_id = '{}' AND receiver_id = '{}') OR (receiver_id = '{}' AND sender_id = '{}')
    """.format(id_user, idfriend, id_user, idfriend))
    r = db.store_result()
    rows = r.fetch_row(maxrows=0)
    print (rows)
    data= [{'sender_id': row[0].decode('utf-8'), 'message': row[1].decode('utf-8')} for row in rows]
    print(data)
    return data


# get_messages("yara@mail.com",2)

# all_messages(1,2)

def save_message(email_sender, receiver_id, message):
    sender_id= get_idfriend_by_mail(email_sender)
    try: 
        db.query("START TRANSACTION")
        db.query("""INSERT INTO message (sender_id, receiver_id, message) VALUES ('{}','{}','{}')""".format(sender_id, receiver_id, message))
        db.query("COMMIT")

    except _mysql.Error as e:
    # En caso de error, revertir la transacción
        print("Error en la transacción:", e)
        db.query("ROLLBACK")
    return db.affected_rows()

save_message("yara@mail.com",2,"jijhgfdsdafghj")
