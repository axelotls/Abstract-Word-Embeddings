import json
import requests
import time
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

abstracts = open("Abstracts.txt", "w", encoding="utf-8")

def main():
    # for example sake, abstracts.txt is cleared every time the code runs
    # if the same topic is searched, there will be repeats
    while True:
        searchTopic = simpledialog.askstring(title="Abstract Retrieval", prompt="Enter a topic to search for: \n\n" + 
        "To search for multiple topics,enter the query as such: \n\nlesion AND pancreatic (equal to lesion-pancreatic and lesion pancreatic)\nkidney OR renal\nganglia OR tumor AND NOT malignan\n", parent=root)
        numOfJournals = simpledialog.askstring(title="Abstract Retrieval", prompt="Enter a number of journals: \n\n\t\t (Enter Max for maximum journal retrieval)", parent=root)
        if numOfJournals == "max":
            numOfJournals = "10000"
        
        try:
            SpringerExtraction(numOfJournals, searchTopic)

        except IndexError as e:
            print("\n[Out of Springer Nature Journals.]")

        except IndexError as e:
            print("\n[Out of Springer Nature Journals.]")

        
        try:
            ElsevierExtraction(numOfJournals, searchTopic)
        except IndexError as e:
            print("\n[Out of Elsevier Journals.]")

        except KeyError() as e:
            print("\n[Out of Elsevier Journals.]")  # KeyError happens when there is also no more indices left.

        print("\n[Abstract Retrieval: Done.]")
    abstracts.close
    quit()


def SpringerJSON(offset, ceiling, searchTopic, numOfJournals):
        # https://dev.springernature.com/adding-constraints
        #KeyWord search: limit to articles tagged with a keyword
        # subject: 	limit to the specified subject collection
        url = requests.get("http://api.springernature.com/meta/v2/json?q=language:en+keyword:" + searchTopic + "&s=" + 
        str(offset)+ "&p=" + str(ceiling) + "&api_key=50fa5bb93bb66d04245858c6490c3293")
        return json.loads(url.text)
        
def ElsevierJSON(offset, ceiling, searchTopic, numOfJournals):
    # https://dev.elsevier.com/sd_article_meta_tips.html
    url = requests.get("https://api.elsevier.com/content/metadata/article?query="
    + "keywords(" + searchTopic + ")" + "&view=COMPLETE&" + "&start=" + str(offset) + "&count=" + str(ceiling) + "&" + 
    "httpAccept=application/json&apiKey=dc1c396604f71b360feeecd6f767e1d4")
    return json.loads(url.text)


def ElsevierExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 0

    if (201 > tempJournals > 0):
        ceiling = tempJournals
        data = ElsevierJSON(offset, ceiling, searchTopic, numOfJournals)
        for i in range(tempJournals):
            if data['search-results']['entry'][i]['dc:description'] == None:
                break
            else:
                abstract = data['search-results']['entry'][i]['dc:description'] + "\n"  # \n isn't required
                abstracts.write(str(abstract).replace("Background", ""))
    else:
        ceiling = 200
        while (tempJournals > 0):
            data = ElsevierJSON(offset, ceiling, searchTopic, numOfJournals)
            for i in range(ceiling):
                if data['search-results']['entry'][i]['dc:description'] == None:
                    break
                else:
                    abstract = data['search-results']['entry'][i]['dc:description'] + "\n"  # \n isn't required
                    abstracts.write(str(abstract).replace("Background", ""))

            offset += 200
            tempJournals -= 200

            if (tempJournals > 200):
                ceiling = 200
            else:
                ceiling = tempJournals
            
            time.sleep(5)

def SpringerExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 1

    if (100 > tempJournals > 0):
        ceiling = tempJournals
        data = SpringerJSON(offset, ceiling, searchTopic, numOfJournals)
        for i in range(0, tempJournals):
            if data['records'][i]['abstract'] != "":
                abstract = data['records'][i]['abstract'] + "\n"  # \n isn't required
                abstracts.write(str(abstract).replace("Background", ""))

    else:
        ceiling = 100
        while (tempJournals > 0):
            data = SpringerJSON(offset, ceiling, searchTopic, numOfJournals)
            for i in range(ceiling):
                i %= 100
                if data['records'][i]['abstract'] != "":
                    abstract = data['records'][i]['abstract'] + "\n"  # \n isn't required
                    abstracts.write(str(abstract).replace("Background", ""))

            offset += 100
            tempJournals -= 100

            if (tempJournals > 100):
                ceiling = 100
            else:
                ceiling = tempJournals
            
            time.sleep(5)

root = tk.Tk()
root.geometry('0x0+1000+400')

root.update_idletasks()
main()
#root.withdraw()
root.mainloop()
