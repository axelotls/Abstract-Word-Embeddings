import json
import requests
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

# for example sake, abstracts.txt is cleared every time the code runs
# if the same topic is searched, there will be repeats
abstracts = open("SpringerNature/springerNatureAbstracts.txt", "w")

def main():
    while True:
        abstracts = open("SpringerNature/springerNatureAbstracts.txt", "a")
        searchTopic = simpledialog.askstring(title="Abstract Retrieval", prompt="Enter a topic to search for: \n\n\t\t", parent=root)
        numOfJournals = simpledialog.askstring(title="Abstract Retrieval", prompt="Enter a number of journals: \n\n\t\t", parent=root)
        extractAbstracts(numOfJournals, searchTopic)
        print("\n[Abstract Retrieval: Done.]")
        if (messagebox.askyesno(title="Abstract Retrieval", message="Finished. \tContinue?", ) == False):
            break
    abstracts.close
    quit()


 
def extractAbstracts(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 1

    if (100 > tempJournals > 0):
        ceiling = tempJournals
        data = urlRequest(offset, ceiling, searchTopic, numOfJournals)
        for i in range(0, tempJournals):
            if data['records'][i]['abstract'] != "":
                abstract = data['records'][i]['abstract'] + "\n"  # \n isn't required
                abstracts.writelines(abstract)

    else:
        ceiling = 100
        while (tempJournals > 0):
            data = urlRequest(offset, ceiling, searchTopic, numOfJournals)
            for i in range(ceiling):
                i %= 100
                if data['records'][i]['abstract'] != "":
                    abstract = data['records'][i]['abstract'] + "\n"  # \n isn't required
                    abstracts.writelines(abstract)

            offset += 100
            tempJournals -= 100

            if (tempJournals > 100):
                ceiling = 100
            else:
                ceiling = tempJournals

def urlRequest(offset, ceiling, searchTopic, numOfJournals):
        url = requests.get("https://api.springernature.com/meta/v2/json?api_key=50fa5bb93bb66d04245858c6490c3293&q=" + 
        str(searchTopic) + "&s=" + str(offset) + "&p=" + str(numOfJournals))
        return json.loads(url.text)

root = tk.Tk()
root.geometry('0x0+1000+400')

root.update_idletasks()
main()
#root.withdraw()
root.mainloop()



