import json
import requests
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

"""
txtdump = open("ScienceDirect", 'w')
txtdump.write(str(url))
 
txtdump.close
"""
abstracts = open("ScienceDirect/Elsevier.txt", "w")
offset = 0


def main():
    while True:
        abstracts = open("ScienceDirect/Elsevier.txt", "a")
        searchTopic = simpledialog.askstring(title="Abstract Retrieval", prompt="Enter a topic to search for: \n\n" + 
        "To search for multiple topics,enter the query as such: \n\nlesion AND pancreatic (equal to lesion-pancreatic and lesion pancreatic)\nkidney OR renal\nganglia OR tumor AND NOT malignan\n", parent=root)
        numOfJournals = simpledialog.askstring(title="Abstract Retrieval", prompt="Enter a number of journals: \n\n\t\t", parent=root)
        extractAbstracts(numOfJournals, searchTopic)
        print("\n[Abstract Retrieval: Done.]")
        if (messagebox.askyesno(title="Abstract Retrieval", message="Finished. \tContinue?", ) == False):
            break
    abstracts.close
    quit()


def extractAbstracts(numOfJournals, searchTopic):
    abstracts = open("ScienceDirect/Elsevier.txt", "a")
    data = urlRequest(offset, searchTopic, numOfJournals)
    for i in range(int(numOfJournals)):
        if data['search-results']['entry'][i]['dc:description'] == None:
            break
        else:
            abstract = data['search-results']['entry'][i]['dc:description'] + "\n"  # \n isn't required
            abstracts.write(str(abstract))
            print(abstract)
    abstracts.close








def urlRequest(offset, searchTopic, numOfJournals):
    url = requests.get("https://api.elsevier.com/content/metadata/article?query="
    + "keywords(" + searchTopic + ")" + "&view=COMPLETE&" + "&start=" + str(offset) + "&count=25&" + "httpAccept=application/json&apiKey=dc1c396604f71b360feeecd6f767e1d4")
    return json.loads(url.text)









root = tk.Tk()
root.geometry('0x0+1000+400')

root.update_idletasks()
main()
#root.withdraw()
root.mainloop()






