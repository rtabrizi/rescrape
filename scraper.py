import bs4 as bs
import urllib.request

url = 'https://openaccess.thecvf.com/CVPR2022?day=all'
sauce = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(sauce, 'lxml')
links = soup.find_all('a', href=True)
paperLinks = []


def contains(substring, string):
    if substring.lower() in string.lower():
        return True
    else:
        return False

for link in links:
    if link.text == 'pdf':
        paperLinks.append(link)

for paper in paperLinks:
    print(paper)
    print()