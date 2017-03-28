from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import re
import requests
import subprocess

base_url  = "http://papers.nips.cc"
index_url = "http://papers.nips.cc/book/advances-in-neural-information-processing-systems-29-2016"

r = requests.get(index_url)

soup = BeautifulSoup(r.content, "lxml")
paper_links = [link for link in soup.find_all('a') if link["href"][:7]=="/paper/"]
print("%d Papers Found" % len(paper_links))

nips_authors = set()
papers = list()
paper_authors = list()

temp_path = os.path.join("output", "temp.txt")

def text_from_pdf(pdf_path, temp_path):
    if os.path.exists(temp_path):
        os.remove(temp_path)
    subprocess.call(["pdftotext", pdf_path, temp_path])
    f = open(temp_path, encoding="utf8")
    text = f.read()
    f.close()
    os.remove(temp_path)
    return text

#for link in paper_links[:5]:
for link in paper_links:
    paper_title = link.contents[0]
    info_link = base_url + link["href"]
    pdf_link = info_link + ".pdf"
    pdf_name = link["href"][7:] + ".pdf"
    paper_id = re.findall(r"^(\d+)-", pdf_name)[0]
    pdf = requests.get(pdf_link)
    pdf_path = os.path.join("output", "pdfs", pdf_name)
    pdf_file = open(pdf_path, "wb")
    pdf_file.write(pdf.content)
    pdf_file.close()
    paper_soup = BeautifulSoup(requests.get(info_link).content, "lxml")
    try: 
        abstract = paper_soup.find('p', attrs={"class": "abstract"}).contents[0]
    except:
        print("Abstract not found %s" % paper_title.encode("ascii", "replace"))
        abstract = ""
    authors = [(re.findall(r"-(\d+)$", author.contents[0]["href"])[0],
                author.contents[0].contents[0])
               for author in paper_soup.find_all('li', attrs={"class": "author"})]
    for author in authors:
        nips_authors.add(author)
        paper_authors.append([len(paper_authors)+1, paper_id, author[0]])
    event_types = [h.contents[0][23:] for h in paper_soup.find_all('h3') if h.contents[0][:22]=="Conference Event Type:"]
    if len(event_types) != 1:
        print(event_types)
        print([h.contents for h in paper_soup.find_all('h3')])
        raise Exception("Bad Event Data")
    event_type = event_types[0]
    paper_text = text_from_pdf(pdf_path, temp_path)
    print(paper_title.encode('ascii', 'namereplace'))
    papers.append([paper_id, paper_title, event_type, pdf_name, abstract, paper_text])

pd.DataFrame(list(nips_authors), columns=["Id","Name"]).to_csv("output/Authors.csv", index=False)
pd.DataFrame(papers, columns=["Id", "Title", "EventType", "PdfName", "Abstract", "PaperText"]).to_csv("output/Papers.csv", index=False)
pd.DataFrame(paper_authors, columns=["Id", "PaperId", "AuthorId"]).to_csv("output/PaperAuthors.csv", index=False)
