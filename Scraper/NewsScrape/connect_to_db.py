import MySQLdb


def connect_to_articlesdb():
    # connect to phpmyadmin and get links and articles
    db = MySQLdb.connect('localhost', 'root', '', 'articleDB', charset='utf8')
    return db.cursor()


def get_link_from_title(title):
    crs = connect_to_articlesdb()
    crs.execute(f"""SELECT link FROM articles WHERE title title = '{title}'""")
    # TODO: Error message if not found
    return crs.fetchall()


def get_all():
    crs = connect_to_articlesdb()
    crs.execute("""SELECT link FROM articles""")
    return crs.fetchall()