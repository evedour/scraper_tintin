import MySQLdb


def connect_to_articlesdb():
    print('Connecting to article database...')
    # connect to phpmyadmin and get links and articles
    db = MySQLdb.connect('localhost', 'root', '', 'articleDB', charset='utf8')
    return db.cursor()


def get_link_from_title(title):
    crs = connect_to_articlesdb()
    print('Getting your article....')
    crs.execute(f"""SELECT link FROM articles WHERE title title = '{title}'""")
    # TODO: Error message if not found
    return crs.fetchall()


def get_all():
    crs = connect_to_articlesdb()
    print('Getting your articles')
    crs.execute("""SELECT link FROM articles""")
    return crs.fetchall()