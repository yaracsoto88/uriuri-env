from MySQLdb import _mysql

db=_mysql.connect("localhost", "root", "", "chat")

def get_user(email, password):
    db.query("""SELECT * FROM user WHERE email='{}' AND password='{}'""".format(email, password))
    r = db.store_result()
    return r.num_rows()

def create_user(email,username,password):
    db.query("""INSERT INTO user (email, username, password) VALUES ('{}','{}','{}')""".format(email,username, password))
    return db.affected_rows()

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

def save_message(email_sender, receiver_id, message):
    sender_id= get_idfriend_by_mail(email_sender)
    try: 
        db.query("START TRANSACTION")
        db.query("""INSERT INTO message (sender_id, receiver_id, message) VALUES ('{}','{}','{}')""".format(sender_id, receiver_id, message))
        db.query("COMMIT")

    except _mysql.Error as e:
        print("Error en la transacción:", e)
        db.query("ROLLBACK")
    return db.affected_rows()

def exists_friend(email_user, email_friend):
    id_user= get_idfriend_by_mail(email_user)
    id_friend= get_idfriend_by_mail(email_friend)
    db.query("""SELECT * FROM userfriend WHERE (user_id='{}' AND friend_id='{}') or (friend_id='{}' AND user_id='{}') """.format(id_user, id_friend, id_user, id_friend))
    r = db.store_result()
    return r.num_rows()
 
def add_friend(email_user, email_friend):
    id_user= get_idfriend_by_mail(email_user)
    id_friend= get_idfriend_by_mail(email_friend)
    if exists_friend(email_user, email_friend) > 0:
        return -1
    try: 
        db.query("START TRANSACTION")
        db.query("""INSERT INTO userfriend (user_id, friend_id) VALUES ('{}','{}')""".format(id_user, id_friend))
        db.query("COMMIT")

    except _mysql.Error as e:
        print("Error en la transacción:", e)
        db.query("ROLLBACK")
    return db.affected_rows()
    
def exists_friend_request(email_user, email_friend):
    id_user= get_idfriend_by_mail(email_user)
    id_friend= get_idfriend_by_mail(email_friend)
    db.query("""SELECT * FROM friend_request WHERE sender_id='{}' AND receiver_id='{}'""".format(id_user, id_friend))
    r = db.store_result()
    return r.num_rows()

def send_friend_request(email_user, email_friend):
    id_user= get_idfriend_by_mail(email_user)
    id_friend= get_idfriend_by_mail(email_friend)
    if exists_friend(email_user, email_friend) > 0 or exists_friend_request(email_user,email_friend):
        return -1
    try: 
        db.query("START TRANSACTION")
        db.query("""INSERT INTO friend_request (sender_id, receiver_id) VALUES ('{}','{}')""".format(id_user, id_friend))
        db.query("COMMIT")

    except _mysql.Error as e:
        print("Error en la transacción:", e)
        db.query("ROLLBACK")
    return db.affected_rows()

def get_friend_request(email_user):
    id_user = get_idfriend_by_mail(email_user)
    db.query("""
        SELECT user.email 
        FROM friend_request 
        INNER JOIN user ON sender_id = user.id 
        WHERE receiver_id = '{}'
    """.format(id_user))
    
    r = db.store_result()
    rows = r.fetch_row(maxrows=0)
    
    emails = [row[0].decode('utf-8') for row in rows]
    return emails

def get_id_friend_by_username(username):
    db.query("""SELECT id FROM user WHERE username = '{}'""".format(username))
    r = db.store_result()
    return r.fetch_row(maxrows=0)[0][0].decode('utf-8')

def accept_friend_request(email_user, friend):
    id_user = get_idfriend_by_mail(email_user)
    id_friend = get_idfriend_by_mail(friend)
    try: 
        db.query("START TRANSACTION")
        db.query("""INSERT INTO userfriend (user_id, friend_id) VALUES ('{}','{}')""".format(id_user, id_friend))
        db.query("""DELETE FROM friend_request WHERE sender_id='{}' AND receiver_id='{}'""".format( id_friend, id_user))
        db.query("COMMIT")

    except _mysql.Error as e:
        print("Error en la transacción:", e)
        db.query("ROLLBACK")
    return db.affected_rows()


def deny_friend_request(email_user, friend):
    id_user = get_idfriend_by_mail(email_user)
    id_friend = get_idfriend_by_mail(friend)
    try: 
        db.query("START TRANSACTION")
        db.query("""DELETE FROM friend_request WHERE sender_id='{}' AND receiver_id='{}'""".format(id_friend, id_user))
        db.query("COMMIT")

    except _mysql.Error as e:
        print("Error en la transacción:", e)
        db.query("ROLLBACK")
    return db.affected_rows()

def get_name(id):
    db.query("""SELECT username FROM user WHERE id = '{}'""".format(id))
    r = db.store_result()
    return r.fetch_row(maxrows=0)[0][0].decode('utf-8')