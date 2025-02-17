import json
import requests
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog
import re
import subprocess
import time

# August Moses VCU 2023

def __main__():
    global DOIs
    DOIs = []
    searchTopic = simpledialog.askstring(
        title="Abstract Retrieval",
        prompt="Current # of abstracts: "
        + "\nEnter a topic to search for: \n\n"
        + "To search for multiple topics,enter the query as such: \n\nlesion AND pancreatic\nkidney AND (tissue OR renal)\nganglia OR tumor AND NOT malignan\n\nNote: Springer Nature doesn't take parenthesis into consideration",
        parent=root,
    )
    numOfJournals = simpledialog.askstring(
        title="Abstract Retrieval",
        prompt="Enter a number of journals:",
        parent=root,
    )

    try:
        RESTAPIExtraction(numOfJournals, searchTopic)
    except (IndexError, KeyError, TypeError) as error:
        pass
    try:
        SpringerExtraction(numOfJournals, searchTopic)
    except (IndexError, KeyError) as error:
        pass
    try:
        ElsevierExtraction(numOfJournals, searchTopic)
    except (IndexError, KeyError) as error:
        pass

    AbsDblCheck()
    doiWriter()
    print(len(abstracts))
    print("Done.")
    abstracts.close()
    quit()


def SpringerJSON(offset, ceiling, searchTopic):
    # https://dev.springernature.com/adding-constraints
    # KeyWord search: limit to articles tagged with a keyword
    # subject: 	limit to the specified subject collection
    if "(" in searchTopic:
        searchTopic.replace("(", "").replace(")", "")
    url = requests.get(
        "http://api.springernature.com/meta/v2/json?q=language:en+keyword:"
        + searchTopic
        + "&s="
        + str(offset)
        + "&p="
        + str(ceiling)
        + "&api_key=50fa5bb93bb66d04245858c6490c3293"
    )
    return json.loads(url.text)


def ElsevierJSON(offset, ceiling, searchTopic):
    # https://dev.elsevier.com/sd_article_meta_tips.html
    url = requests.get(
        "https://api.elsevier.com/content/metadata/article?query="
        + "keywords("
        + searchTopic
        + ")"
        + "&view=COMPLETE&"
        + "&start="
        + str(offset)
        + "&count="
        + str(ceiling)
        + "&"
        + "httpAccept=application/json&apiKey=dc1c396604f71b360feeecd6f767e1d4"
    )
    return json.loads(url.text)


def RESTAPIJSON(offset, ceiling, searchTopic):
    url = requests.get(
        "https://api.crossref.org/works?query= "
        + searchTopic
        + " &rows="
        + str(ceiling)
        + "&offset="
        + str(offset)
        + "&filter=has-abstract:true&mailto=mosesa3@vcu.edu"
    )
    return json.loads(url.text)


def ElsevierExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 0

    if 200 > tempJournals > 0:
        ceiling = tempJournals
        data = ElsevierJSON(offset, ceiling, searchTopic)
        ElsevierParser(ceiling, data)

    if tempJournals > 200:
        ceiling = 200
        while tempJournals > 0:
            data = ElsevierJSON(offset, ceiling, searchTopic)
            ElsevierParser(ceiling, data)

            offset += 200
            tempJournals -= 200

            if tempJournals > 200:
                ceiling = 200
            else:
                ceiling = tempJournals


def ElsevierParser(ceiling, data):
    for i in range(ceiling):
        i %= 100
        if data["search-results"]["entry"][i]["dc:description"] == None:
            continue
        else:
            doi = str(data["search-results"]["entry"][i]["dc:identifier"]).replace(
                "DOI:", ""
            )
            if DuplicateCheck(doi) == False:
                abstract = (
                    str(data["search-results"]["entry"][i]["dc:description"]).replace(
                        "Background", ""
                    )
                    + "\n"
                )
                fileWriter(abstract)


def SpringerExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 1

    if 100 > tempJournals > 0:
        ceiling = tempJournals
        data = SpringerJSON(offset, ceiling, searchTopic)
        SpringerParser(ceiling, data)

    else:
        ceiling = 100
        while tempJournals > 0:
            data = SpringerJSON(offset, ceiling, searchTopic)
            SpringerParser(ceiling, data)

            offset += 100
            tempJournals -= 100

            if tempJournals > 100:
                ceiling = 100
            else:
                ceiling = tempJournals


def SpringerParser(ceiling, data):
    for i in range(ceiling):
        i %= 100
        try:
            if (
                data["records"][i]["abstract"] == ""
                or data["records"][i]["abstract"] == None
            ):
                continue
            else:
                doi = data["records"][i]["identifier"].replace("doi:", "")
                if DuplicateCheck(doi) == False:
                    abstract = data["records"][i]["abstract"] + "\n"
                    fileWriter(abstract)
        except:
            pass


def RESTAPIExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 0

    if tempJournals <= 1000:
        ceiling = tempJournals
        data = RESTAPIJSON(offset, ceiling, searchTopic)
        RESTAPIparser(ceiling, data)

    else:
        ceiling = 1000
        while tempJournals > 0:
            data = RESTAPIJSON(offset, ceiling, searchTopic)
            RESTAPIparser(ceiling, data)

            offset += 1000
            tempJournals -= 1000

            if tempJournals > 1000:
                continue
            else:
                RESTAPIExtraction(tempJournals, searchTopic)


def RESTAPIparser(ceiling, data):
    for item in data["message"]["items"]:
        doi = item["DOI"]
        if DuplicateCheck(doi) == False:
            abstract = item["abstract"]
            abstract = re.sub("<\S+>", "", abstract)
            abstract = re.sub("[a-z]*&\S*;", "", abstract)
            abstract = re.sub("\s{2,}", "", abstract)
            abstract = re.sub("\n", " ", abstract)
            abstract += "\n"
            fileWriter(abstract)


def fileWriter(abstract):
    with open("AbstractRetrieval\Data.txt", "a", encoding="utf-8") as fn:
        fn.write(abstract)


def doiWriter():
    with open("AbstractRetrieval\log.txt", "w", encoding="utf-8") as fn:
        for i in DOIs:
            fn.write(i + "\n")


def DuplicateCheck(doi):
    if doi in DOIs:
        return True
    else:
        DOIs.append(doi)
        return False

def AbsDblCheck():
    data = [line.strip() for line in open("./Data.txt", 'r')]
    abstracts = list(set(data))

    with open("Abstracts.txt", "w", encoding="utf-8") as fn:
            for value in abstracts:
                fn.write(value + "\n")

root = tk.Tk()
root.geometry("10x10+1000+400")
root.update_idletasks()
__main__()
root.mainloop()
