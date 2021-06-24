import binascii
import os
import sqlite3 as sql
import hashlib


def insert_todo(**data):
    con = sql.connect("database.db")
    try:
        name = str(tuple(data.keys()))
        name = name.replace('\'', '')
        # cur = con.cursor()
        con.execute("INSERT INTO todo {} VALUES {}".format(name, tuple(data.values())))
        con.commit()
        return True, 'data successfully added'
    except:
        con.rollback()
        return False, 'data Failed added'


def insert_user(**data):
    con = sql.connect("database.db")
    try:
        if check_email(data['email']):
            return False, 'An email already exists Please enter a new email'
        if check_username(data['username']):
            return False, 'username already exists Please enter a new username'
        # cur = con.cursor()
        data['password'] = hash_password(data['password'])
        print(data['password'])

        name = str(tuple(data.keys()))
        name = name.replace('\'', '')
        print(tuple(data.values()))
        print(name)
        con.execute("INSERT INTO user {} VALUES {}".format(name, tuple(data.values())))
        print('data added')
        con.commit()
        return True, 'account successfully created'
    except:
        con.close()
        return False, 'account created Failed'


def login_user(**data):
    con = sql.connect("database.db")
    user_data = {}
    try:
        cursor = con.execute("select id , email, password from user where email = '{}' ".format(data['email']))
        for row in cursor :
            user_data['id'] = row[0]
            user_data['email'] = row[1]
            user_data['password'] = row[2]
    except:
        con.rollback()
        return False, 'your email  is wrong please check your email'

    try:
        if verify_password(user_data['password'], data['password']):
            return True, user_data['id']
        else:
            return False, 'please enter valid password'
    except:
        return False, 'please enter valid password'


def check_email(email):
    with sql.connect("database.db") as con:
        # cur = con.cursor()
        cursor = con.execute("select email from user where email = '{}'".format(email))

        if cursor.row_factory is not None:
            return True
        else:
            return False


def check_username(username):
    with sql.connect("database.db") as con:
        # cur = con.cursor()
        cursor = con.execute("select username from user where username = '{}'".format(username))
        if  cursor.row_factory is not None:
            return True
        else:
            return False


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, entered_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  entered_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def get_users():
    with sql.connect("database.db") as con:
        # cur = con.cursor()
        cursor = con.execute("select * from user")
        user = []
        for row in cursor :
            data={}
            data['id'] = row[0]
            data['username'] = row[1]
            data['email'] = row[2]
            data['password'] = row[3]
            user.append(data)
        print(user)


def get_todo_incomplete(user_id):
    with sql.connect("database.db") as con:
        # cur = con.cursor()
        cursor = con.execute("select id, body, type, created from todo where type = 0 and author_id = {}".format(user_id))
        todo_list = list()

        for row in cursor:
            data = dict()
            data['id'] = row[0]
            data['body'] = row[1]
            data['type'] = row[2]
            data['created'] = row[3]
            todo_list.append(data)
        return todo_list


def get_todo_complete(user_id):
    with sql.connect("database.db") as con:
        # cur = con.cursor()
        cursor = con.execute("select id, body, type, created from todo where type = 1 and author_id = {}".format(user_id))
        todo_list = list()

        for row in cursor:
            data = dict()
            data['id'] = row[0]
            data['body'] = row[1]
            data['type'] = row[2]
            data['created'] = row[3]
            todo_list.append(data)
        return todo_list


def delete(todo_id):
    con = sql.connect("database.db")
    try:
        con.execute("delete from todo where id = {}".format(todo_id))
        con.commit()
        return True, 'Todo Item deleted Successfully'
    except:
        return False, 'Todo Item deleted Failed'


def update(todo_id):
    con = sql.connect("database.db")
    try:
        todo_type = get_todo_by_id(todo_id)[2]
        if todo_type == '1':
            con.execute("update todo set type = {} where id = {}".format('0', todo_id))
            con.commit()
            return True, 'Todo Item updated Successfully'
        elif todo_type == '0':
            con.execute("update todo set type = {} where id = {}".format('1', todo_id))
            con.commit()
            return True, 'Todo Item updated Successfully'
    except:
        return False, 'Todo Item updated Failed'


def get_todo_by_id(todo_id):
    with sql.connect("database.db") as con:
        # cur = con.cursor()
        cursor = con.execute("select id, body, type, created from todo where id = {}".format(todo_id))
        # todo_list = list()
        # data = dict()
        # for row in cursor:
        #     data['id'] = row[0]
        #     data['body'] = row[1]
        #     data['type'] = row[2]
        #     data['created'] = row[3]
        return cursor.fetchone()


# print(get_todo_incomplete())
# print(type(get_todo_by_id(5)[2]))

