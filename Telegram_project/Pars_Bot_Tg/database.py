import sqlite3


def get_connection_base_data(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('subscribers.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connection_base_data
def get_data(conn, clear: bool = False):
    c = conn.cursor()
    if clear:
        c.execute("DROP TABLE IF EXISTS event_sub")
    c.execute("""CREATE TABLE IF NOT EXISTS event_sub(
        user_id INTEGER,
        last_data_ivent INTEGER,
        price TEXT,
        last_data_text TEXT, 
        link_text TEXT,
        link_image TEXT
    )""")
    conn.commit()


@get_connection_base_data
def set_user_id(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT user_id FROM event_sub WHERE user_id = ?", (user_id, ))
    if c.fetchone() is None:
        c.execute("INSERT INTO event_sub(user_id, last_data_ivent) VALUES (?, ?)", (user_id, 0))
        conn.commit()


@get_connection_base_data
def set_data_ivent(conn, data_ivent, user_id, data_text):
    c = conn.cursor()
    c.execute("UPDATE event_sub SET last_data_ivent = ? WHERE user_id = ?", (data_ivent, user_id))
    conn.commit()
    c.execute("UPDATE event_sub SET last_data_text = ? WHERE user_id = ?", (data_text, user_id))
    conn.commit()


@get_connection_base_data
def set_data_links(conn, link, link_image, user_id):
    c = conn.cursor()
    c.execute("UPDATE event_sub SET link_text = ? WHERE user_id = ?", (link, user_id))
    conn.commit()
    c.execute("UPDATE event_sub SET link_image = ? WHERE user_id = ?", (link_image, user_id))
    conn.commit()


@get_connection_base_data
def set_price(conn, user_id, price):
    c = conn.cursor()
    c.execute("UPDATE event_sub SET price = ? WHERE user_id = ?", (price, user_id))
    conn.commit()


@get_connection_base_data
def get_data_ivent(conn, user_id):
    c = conn.cursor()
    ivent = []
    c.execute("SELECT last_data_ivent FROM event_sub WHERE user_id = ?", (user_id, ))
    ivent.append(c.fetchone()[0])
    c.execute("SELECT last_data_text FROM event_sub WHERE user_id = ?", (user_id, ))
    ivent.append(c.fetchone()[0])
    return ivent


@get_connection_base_data
def get_data_link(conn, user_id):
    c = conn.cursor()
    links = []
    c.execute("SELECT link_text FROM event_sub WHERE user_id = ?", (user_id, ))
    links.append(c.fetchone()[0])
    c.execute("SELECT link_image FROM event_sub WHERE user_id = ?", (user_id, ))
    links.append(c.fetchone()[0])
    return links


@get_connection_base_data
def get_price(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT price FROM event_sub WHERE user_id = ?", (user_id,))
    price = c.fetchone()[0]
    return price
