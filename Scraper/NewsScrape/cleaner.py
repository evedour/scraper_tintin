from bs4 import BeautifulSoup


def get_politico():
    with open('Results/news_www.politico.eu.html', 'rb')as politico:
        soup = BeautifulSoup(politico, 'html.parser')
    paragraphs = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text
        link = item.link.next
        encoded = item.findAll(text=True)
        content = []
        isitcontent = []
        for cd in encoded:
            if isinstance(cd, BeautifulSoup.Cdata):
                content.append(cd)
        print('')
    print('Done: Politico')


def get_euronews():
    print('Done: Euronews')


def get_washington_post():
    print('Done: Washington Post')


def get_bbc():
    print('Done: BBC')


def get_html_text():
    get_politico()
    # get_euronews()
    # get_washington_post()
    # get_bbc()
