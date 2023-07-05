import json
import requests
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog
import re
import subprocess

## August Moses VCU 2023 
# pyinstaller --onefile -w 'AbstractRetrieval.py'
abstracts = open("Abstracts.txt", "w", encoding="utf-8")
def __main__():
    count = 0
    # for example sake, abstracts.txt is cleared every time the code runs
    while True:
        try:
            count = counter(count)
            searchTopic = simpledialog.askstring(title="Abstract Retrieval", prompt="Current lines of abstracts: " + str(counter(count)) + "\nEnter a topic to search for: \n\n" + 
            "To search for multiple topics,enter the query as such: \n\nlesion AND pancreatic\nkidney AND (tissue OR renal)\nganglia OR tumor AND NOT malignan\n\nNote: Springer Nature doesn't take parenthesis into consideration", 
            parent=root)
            numOfJournals = simpledialog.askstring(title="Abstract Retrieval", 
            prompt="Enter a number of journals:", parent=root)
            abstracts = open("Abstracts.txt", "a")
            
            try:
                RESTAPIExtraction(numOfJournals, searchTopic)
            except (IndexError, KeyError) as error:
                continue

            try:
                SpringerExtraction(numOfJournals, searchTopic)
            except (IndexError, KeyError) as error:
                continue         

            try:
                ElsevierExtraction(numOfJournals, searchTopic)
            except (IndexError, KeyError) as error:
                continue

            abstracts.close()


        except (TypeError) as error:
            subprocess.run(['open', 'Abstracts.txt'], check=True)
            abstracts.close
            break
    


def SpringerJSON(offset, ceiling, searchTopic):
    # https://dev.springernature.com/adding-constraints
    #KeyWord search: limit to articles tagged with a keyword
    # subject: 	limit to the specified subject collection
    if "(" in searchTopic:
        searchTopic.replace("(", "").replace(")", "")
    url = requests.get("http://api.springernature.com/meta/v2/json?q=language:en+keyword:" + searchTopic + "&s=" + 
    str(offset)+ "&p=" + str(ceiling) + "&api_key=50fa5bb93bb66d04245858c6490c3293")
    return json.loads(url.text)
        
def ElsevierJSON(offset, ceiling, searchTopic):
    # https://dev.elsevier.com/sd_article_meta_tips.html
    url = requests.get("https://api.elsevier.com/content/metadata/article?query="
    + "keywords(" + searchTopic + ")" + "&view=COMPLETE&" + "&start=" + str(offset) + "&count=" + str(ceiling) + "&" + 
    "httpAccept=application/json&apiKey=dc1c396604f71b360feeecd6f767e1d4")
    return json.loads(url.text)

def RESTAPIJSON(offset, ceiling, searchTopic):
    url = requests.get("https://api.crossref.org/works?query= " + searchTopic 
    + " &rows=" + str(ceiling) + "&offset=" + str(offset) + "&filter=has-abstract:true&mailto=mosesa3@vcu.edu")
    return json.loads(url.text)

def ElsevierExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 0

    if (201 > tempJournals > 0):
        ceiling = tempJournals
        data = ElsevierJSON(offset, ceiling, searchTopic)
        ElsevierParser(ceiling, data)

    else:
        ceiling = 200
        while (tempJournals > 0):
            data = ElsevierJSON(offset, ceiling, searchTopic)
            ElsevierParser(ceiling, data)
            offset += 200
            tempJournals -= 200

            if (tempJournals > 200):
                ceiling = 200
            else:
                ceiling = tempJournals

def ElsevierParser(ceiling, data):
    for i in range(ceiling):
        if data['search-results']['entry'][i]['dc:description'] == None:
            break
        else:
            abstract = data['search-results']['entry'][i]['dc:description'] + "\n"
            abstracts.write(str(abstract).replace("Background", ""))

def SpringerExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 1

    if (100 > tempJournals > 0):
        ceiling = tempJournals
        data = SpringerJSON(offset, ceiling, searchTopic)
        SpringerParser(ceiling, data)

    else:
        ceiling = 100
        while (tempJournals > 0):
            data = SpringerJSON(offset, ceiling, searchTopic)
            SpringerParser(ceiling, data)

            offset += 100
            tempJournals -= 100

            if (tempJournals > 100):
                ceiling = 100
            else:
                ceiling = tempJournals
                        
def SpringerParser(ceiling, data):
    for i in range(ceiling):
        i %= 100
        if data['records'][i]['abstract'] == "" or data['records'][i]['abstract'] == None:
            break
        else:
            abstract = data['records'][i]['abstract'] + "\n"
            abstracts.write(str(abstract).replace("Background", ""))

def RESTAPIExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 1

    if (tempJournals < 1001):
        ceiling = tempJournals
        data = RESTAPIJSON(offset, ceiling, searchTopic)
        RESTAPIparser(ceiling, data)

    else:
        ceiling = 1000
        while (tempJournals > 0):
            data = RESTAPIJSON(offset, ceiling, searchTopic)
            RESTAPIparser(ceiling, data)

            offset += 1000
            tempJournals -= 1000

            if (tempJournals > 1000):
                ceiling = 1000
            else:
                ceiling = tempJournals

def RESTAPIparser(ceiling, data):
    for i in range(ceiling):
        abstract = data['message']['items'][i]['abstract']
        abstract = re.sub("<\S+>", "", abstract)
        abstract = re.sub("[a-z]*&\S*;", "", abstract)
        abstract = re.sub("\s{2,}", "", abstract)
        abstracts.write(abstract)


def counter(count):
    r_abstracts = open("Abstracts.txt", "r")
    for line in r_abstracts:
        count += 1
    r_abstracts.close()
    return count


root = tk.Tk()
root.geometry('0x0+1000+400')
root.update_idletasks()
__main__()
#root.withdraw()
root.mainloop()
