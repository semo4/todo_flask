import sqlite3
from sqlite3 import Error
import click

from flask import current_app, g
from flask.cli import with_appcontext


# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#     return g.db
#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()
#
#
# def init_db():
#     db = get_db()
#
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
#
#
# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_user():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE user ( id INTEGER PRIMARY KEY AUTOINCREMENT, '
                 'username TEXT UNIQUE NOT NULL,'
                 ' email TEXT UNIQUE NOT NULL,'
                 'password TEXT NOT NULL)')
    print("Table created successfully")


def create_todo():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                 'author_id INTEGER NOT NULL,'
                 'created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
                 'body TEXT NOT NULL,'
                 'type varchar(1) NOT NULL,'
                 'FOREIGN KEY (author_id) REFERENCES user (id))')
    print("Table created successfully")


# create_connection('database.db')
create_user()
create_todo()



