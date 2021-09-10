import MySQLdb


def connect_to_articlesdb():
    print('Connecting to article database...')
    # connect to phpmyadmin and get links and articles
    db = MySQLdb.connect('localhost', 'root', '', 'articleDB', charset='utf8')
    return db.cursor()


def get_all():
    crs = connect_to_articlesdb()
    print('Getting your articles')
    crs.execute("""SELECT link FROM articles""")
    return crs.fetchall()
