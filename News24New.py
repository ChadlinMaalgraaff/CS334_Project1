from bs4 import BeautifulSoup
import requests

# ------------------------------------------------------------------------------


def displayPage(headline, pTags):
    print(' ')
    print(str(headline) + '\n' + '_'*len(headline) + '\n')
    for p in pTags:
        print(str(p.text))
        print(' ')

# ------------------------------------------------------------------------------


pageError = False
try:
    requestWeb = requests.get('https://www.news24.com/TopStories')
    requestMobile = requests.get('http://m.news24.com/Pages/MostRead')
except:
    print("An error occured trying to connect to News24.")
    pageError = True

if (pageError != True):
    soupWeb = BeautifulSoup(requestWeb.text, 'html.parser')
    soupMobile = BeautifulSoup(requestMobile.text, 'html.parser')

    topStoriesDivWeb = soupWeb.find('div', attrs={'class': 'fb_topstories'})
    linksWeb = topStoriesDivWeb.find_all('a')
    url = linksWeb[0].attrs['href']

    try:
        requestMostRead = requests.get(url)
    except:
        print("An error occured trying to connect to most read page.")
        pageError = True

    if (pageError != True):
        soupMostRead = BeautifulSoup(requestMostRead.text, 'html.parser')

        all_p_tags = soupMostRead.find_all('p')

        articleBodyText_pTags = []

        for tag in all_p_tags:
            if (tag.find('a') == None and tag.find('live') == None and tag.find('img') == None and tag.find('span') == None):
                articleBodyText_pTags.append(tag)

# ------------------------------------------------------------------------------

    linksMobile = []
    for link in soupMobile.select('[href]'):
        linksMobile.append(link['href'])

    urlMobile = linksMobile[9]

    try:
        requestMostReadMobile = requests.get(urlMobile)
    except:
        print("An error occured trying to connect to most read page.")
        pageError = True

    if (pageError != True):
        soupMostReadMobile = BeautifulSoup(
            requestMostReadMobile.text, 'html.parser')

        all_p_tagsMobile = soupMostReadMobile.find_all('p')

        articleBodyText_pTagsMobile = []
        artcleHeading = soupMostReadMobile.find('h1').text

        for tag in all_p_tagsMobile:
            if (tag.find('a') == None and tag.find('img') == None):
                articleBodyText_pTagsMobile.append(tag)

        displayPage(artcleHeading, articleBodyText_pTagsMobile)

# ------------------------------------------------------------------------------
