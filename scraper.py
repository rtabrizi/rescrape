import bs4 as bs
import urllib.request
import requests
import re
import io
from PyPDF2 import PdfFileReader

url = 'https://openaccess.thecvf.com/CVPR2022?day=all'
sauce = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(sauce, 'lxml')
links = soup.find_all('a', href=True)
paperLinks = []
domain = "https://openaccess.thecvf.com"
for link in links:
    if link.text == 'pdf':
        paperLinks.append(domain + link['href'])
results = []
def info(pdf_path, results):
 
    # used get method to get the pdf file
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
        pos1 = "UC Berkeley"
        pos2 = "University of California, Berkeley"
        inHeader = pos1 in header or pos2 in header
        inFootNote = pos1 in footNote or pos2 in footNote
        if inHeader or inFootNote and pdf_path not in results:
            print("MATCH FOUND!")
            results.append(pdf_path)
            with open('outputs.txt', 'a') as outputFile:
                outputFile.write(f"{pdf_path}\n")
                outputFile.close()
counter = 1
for i in paperLinks:
    info(i, results)
    print(counter)
    counter += 1
