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
    if conference == 'CVPR':
        print('CVPR')
        scrapeCVPR(year, queries)


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
                findQuery(link, year, queries, results)
                pdfCount += 1
    else:
        print("not yet accounted for")

def findQuery(pdf_path, year, queries, results):
    # used get method to get the pdfile
    response = requests.get(pdf_path)
    # response.content generate binary code for
    # string function
    with io.BytesIO(response.content) as f:
        # initialized the pdf
        pdf = PdfFileReader(f)
        firstPage = pdf.getPage(0)
        text = firstPage.extractText()
        header = text[:400]
        footNote = text[-100:]
        if any([query in header or query in footNote for query in queries]):
            print("MATCH FOUND: %s" % pdf_path)
            results.append(pdf_path)
            with open('CVPR%soutputs.txt' % str(year), 'a') as outputFile:
                outputFile.write(f"{pdf_path}\n")
                outputFile.close()