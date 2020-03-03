from bs4 import BeautifulSoup
import requests

# ------------------------------------------------------------------------------


# Neatly displays the page
def displayPage(headline, pTags):
    print(' ')
    print(str(headline) + '\n' + '_'*len(headline) + '\n')
    for p in pTags:
        print(str(p.text))
        print(' ')

# ------------------------------------------------------------------------------


# Web version
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
        requestMostRead = requests.get(str(url))
    except:
        print("An error occured trying to connect to most read page.")
        pageError = True

    if (pageError != True):
        soupMostRead = BeautifulSoup(requestMostRead.text, 'html.parser')

        try:
            divArticleBody = soupMostRead.find(
                'div', attrs={'class': 'article'})
        except:
            pageError = True

        if (pageError != True):

            articleBodyText_pTagsWeb = []

            if (divArticleBody != None):
                article_p_tags = divArticleBody.find_all('p')

                for tag in article_p_tags:
                    if (tag.find('a') == None):
                        articleBodyText_pTagsWeb.append(tag)

                headlineWeb = divArticleBody.find('h1')

                #displayPage(headlineWeb.text, articleBodyText_pTagsWeb)

# ------------------------------------------------------------------------------

    # Mobile version
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
        artcleHeading = soupMostReadMobile.find('h1')

        for tag in all_p_tagsMobile:
            if (tag.find('a') == None and tag.find('img') == None):
                articleBodyText_pTagsMobile.append(tag)

        displayPage(artcleHeading.text, articleBodyText_pTagsMobile)

# ------------------------------------------------------------------------------
