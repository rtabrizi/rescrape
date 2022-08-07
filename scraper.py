import bs4 as bs
import urllib.request
import requests
import io
from PyPDF2 import PdfFileReader


# url = 'https://openaccess.thecvf.com/CVPR2021?day=all'
# url2 = "https://www.ecva.net/papers.php"
# sauce = urllib.request.urlopen(url).read()
# soup = bs.BeautifulSoup(sauce, 'lxml')
# links = soup.find_all('a', href=True)
# paperLinks = []
# domain = "https://openaccess.thecvf.com"
# for link in links:
#     if link.text == 'pdf':
#         paperLinks.append(domain + link['href'])
# results = []

def scrapeConference(conference, year, queries):
    print ("Now scraping %s %s with the following queries: %s" % (conference, year, queries))
    if conference == 'CVPR':
        scrapeCVPR(year, queries)
    elif conference == 'ICML':
        scrapeICML(year, queries)


def scrapeCVPR(year, queries):
    url = 'https://openaccess.thecvf.com/CVPR%s?day=all' % year
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    if year >= 2021:
        links = soup.find_all('a', href=True)
        domain = "https://openaccess.thecvf.com"
        results = []
        pdfCount = 1
        for link in links:
            if link.text == 'pdf':
                link = domain + link['href']
                print(pdfCount)
                findQuery(link, 'CVPR', year, queries, results)
                pdfCount += 1
    else:
        print("not yet accounted for")

def scrapeICML(year, queries):
    yearToLink = {}
    yearToLink[2022] = "https://proceedings.mlr.press/v162/"
    url = yearToLink[year]
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    links = soup.find_all('a', href=True)
    domain = url
    results = []
    pdfCount = 1
    for link in links:
        if link.text == 'Download PDF':
            print("PDF %s" % pdfCount)
            link = link['href']
            findQuery(link, 'ICML', year, queries, results)
            pdfCount += 1

def findQuery(pdf_path, conference, year, queries, results):
    # used get method to get the pdfile
    response = requests.get(pdf_path)
    # response.content generate binary code for
    # string function
    f = io.BytesIO(response.content)
    with io.BytesIO(response.content) as f:
        # initialized the pdf
        pdf = PdfFileReader(f)
        firstPage = pdf.getPage(0)
        text = firstPage.extractText()
        header = text[:400]
        footNote = text[-100:]
        print(text[600:1000])
        if any([query in text for query in queries]):
            print("MATCH FOUND: %s" % pdf_path)
            print("%s %s" % (conference, pdf_path))
            results.append(pdf_path)
            with open('%s%soutputs.txt' % (conference, str(year)), 'a') as outputFile:
                outputFile.write(f"{pdf_path}\n")
                outputFile.close()
