import sqlite3
from random import randint


def get_connection_base_data(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('job_telegram.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connection_base_data
def create_users_database(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
                 user_id INTEGER NOT NULL,
                 tg_name TEXT,
                 in_channel INTEGER DEFAULT 1,
                 last_ivent TEXT,
                 start_ivent_catalog INTEGER DEFAULT 0,
                 end_ivent_catalog INTEGER DEFAULT 0,
                 start_ivent_incataog INTEGER DEFAULT 0,
                 end_ivent_incatalog INTEGER DEFAULT 0,
                 start_ivent_post INTEGER DEFAULT 0,
                 end_ivent_post INTEGER DEFAULT 0)''')
    conn.commit()


@get_connection_base_data
def create_contents_database(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contents(
                 hashetg TEXT NOT NULL,
                 name_post TEXT NOT NULL,
                 url TEXT,
                 post TEXT NOT NULL,
                 id_post INTEGER NOT NULL
             )''')
    conn.commit()


@get_connection_base_data
def set_users_values(conn, user_id, tg_name):
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id, ))
    if c.fetchone() == None:
        c.execute('''INSERT INTO users(user_id, tg_name) VALUES (?, ?)''', (user_id, tg_name))
        conn.commit()


@get_connection_base_data
def set_last_ivent(conn, last_ivent, chat_id):
    c = conn.cursor()
    c.execute('''UPDATE users SET last_ivent = ? WHERE user_id = ?''', (last_ivent, chat_id))
    conn.commit()


@get_connection_base_data
def set_ivent_catalogs(conn, ivent, chat_id, a_start, a_end):
    c = conn.cursor()
    if ivent == 'catalog':
        c.execute('''UPDATE users SET start_ivent_catalog = ?, end_ivent_catalog = ? WHERE user_id = ?''', (a_start, a_end, chat_id))
        conn.commit()
    elif ivent == 'incatalog':
        c.execute('''UPDATE users SET start_ivent_incataog = ?, end_ivent_incatalog = ? WHERE user_id = ?''', (a_start, a_end, chat_id))
        conn.commit()
    elif ivent == 'post':
        c.execute('''UPDATE users SET start_ivent_post = ?, end_ivent_post = ? WHERE user_id = ?''', (a_start, a_end, chat_id))
        conn.commit()


@get_connection_base_data
def get_last_ivent_catalogs(conn, ivent, chat_id):
    c = conn.cursor()
    if ivent == 'catalog':
        c.execute('''SELECT start_ivent_catalog, end_ivent_catalog FROM users WHERE user_id = ?''', (chat_id,))
    elif ivent == 'incatalog':
        c.execute('''SELECT start_ivent_incataog, end_ivent_incatalog FROM users WHERE user_id = ?''', (chat_id,))
    elif ivent == 'post':
        c.execute('''SELECT start_ivent_post, end_ivent_post FROM users WHERE user_id = ?''', (chat_id,))
    a = c.fetchone()
    if a != None:
        return a
    else:
        return None


@get_connection_base_data
def get_last_ivent(conn, chat_id):
    c = conn.cursor()
    c.execute('SELECT last_ivent FROM users WHERE user_id = ?', (chat_id,))
    a = c.fetchone()
    return a


@get_connection_base_data
def set_contents_value(conn, teg, name_post, url, content):
    c = conn.cursor()
    id_post = randint(1, 50000)
    a, d = True, 0
    while a:
        c.execute('SELECT id_post FROM contents')
        b = c.fetchall()
        if b != None:
            for i in b:
                if i[0] == id_post:
                    id_post = randint(1, 50000)
                    d += 1
                    break
        if d == 0:
            a = False
    c.execute('SELECT hashetg, post FROM contents WHERE hashetg = ? AND post = ?', (teg, content))
    if c.fetchone() == None:
        c.execute('''INSERT INTO contents VALUES (?, ?, ?, ?, ?)''', (teg, name_post, url, content, id_post))
        conn.commit()


@get_connection_base_data
def get_users_values(conn):
    c = conn.cursor()
    subs = []
    c.execute('SELECT user_id, tg_name FROM users')
    a = c.fetchall()
    if len(a) > 0:
        for i in a:
            subs.append(i)
    return subs


@get_connection_base_data
def get_contents_value(conn):
    c = conn.cursor()
    contents = []
    c.execute('SELECT hashetg, name_post, id_post, url FROM contents')
    a = c.fetchall()
    if len(a) > 0:
        for i in a:
            contents.append(i)
    return contents


@get_connection_base_data
def get_url(conn, name_post=None, id_post=None):
    c = conn.cursor()
    if name_post != None and id_post == None:
        c.execute('''SELECT url FROM contents WHERE name_post = ?''', (name_post, ))
    elif id_post != None and name_post == None:
        c.execute('''SELECT name_post, url FROM contents WHERE id_post = ?''', (id_post, ))
    a = c.fetchone()
    if a == None:
        a = 'Ничего не найдено'
    return a


@get_connection_base_data
def get_tegs(conn, ivent=None):
    c = conn.cursor()
    contents = []
    c.execute('SELECT hashetg FROM contents')
    a = c.fetchall()
    if len(a) > 0:
        for i in a:
            if ivent != None:
                if ivent in i[0]:
                    contents.append(i[0])
            else:
                contents.append(i[0])
    return contents


@get_connection_base_data
def get_post_teg_value(conn, teg):
    c = conn.cursor()
    contents = []
    c.execute('SELECT hashetg, post, id_post, url FROM contents WHERE hashetg = ?', (teg, ))
    a = c.fetchall()
    if len(a) > 0:
        for i in a:
            contents.append(i)
    return contents


@get_connection_base_data
def update_update_post(conn, id_post, post=None, url=None):
    c = conn.cursor()
    if post != None and url == None:
        c.execute('UPDATE contents SET post = ? WHERE id_post = ?', (post, id_post))
    elif url != None and post == None:
        c.execute('UPDATE contents SET url = ? WHERE id_post = ?', (url, id_post))
    conn.commit()


@get_connection_base_data
def get_id_post(conn, id_post):
    c = conn.cursor()
    c.execute('SELECT name_post, post FROM contents WHERE id_post = ?', (id_post, ))
    post = c.fetchone()
    if post != None:
        return post
    else:
        return 'Ничего не найдено'


@get_connection_base_data
def get_name_teg(conn, teg=None):
    c = conn.cursor()
    c.execute('SELECT name_post FROM contents WHERE hashetg = ?', (teg, ))
    a = c.fetchall()
    return a


@get_connection_base_data
def get_name_post(conn, name_post):
    c = conn.cursor()
    c.execute('SELECT post FROM contents WHERE name_post = ?', (name_post, ))
    a = c.fetchone()
    return a


@get_connection_base_data
def delete_id_post(conn, id_post):
    c = conn.cursor()
    c.execute('SELECT name_post, post FROM contents WHERE id_post = ?', (id_post, ))
    if c.fetchone() != None:
        c.execute('DELETE FROM contents WHERE id_post = ?', (id_post, ))
        conn.commit()


@get_connection_base_data
def delete_cat_posts(conn, teg):
    c = conn.cursor()
    c.execute('SELECT name_post FROM contents WHERE hashetg = ?', (teg, ))
    if c.fetchone() != None:
        c.execute('''DELETE FROM contents WHERE hashetg = ?''', (teg, ))
        conn.commit()


@get_connection_base_data
def delete_users(conn):
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE in_channel = 0')
    conn.commit()


@get_connection_base_data
def delete_database(conn):
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS contents')

