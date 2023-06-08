import json
import requests

"""
txtdump = open("ScienceDirect", 'w')
txtdump.write(str(url))
 
txtdump.close
"""
abstracts = open("Abstracts/springerNatureAbstracts.txt", "w")

data = json.loads(url.text)
print(str(data))

def extractAbstracts(numOfPages):
    abstracts = open("Abstracts/springerNatureAbstracts.txt", "a")
    for i in range(numOfPages):
        if data['records'][i]['abstract'] != "":
            abstract = data['records'][i]['abstract'] + "\n"  # \n isn't required
            abstracts.writelines(abstract)
            print(abstract)
    abstracts.close    

userInput = ""
while userInput != "A":
    searchTopic = input("Enter a topic to search for: ")
    numOfPages = input("Enter a number of pages to search through (max=100): ")

    url = requests.get("https://api.elsevier.com/content/metadata/article?query=aff(broad%20institute)%20and%20pub-date%20is%202014&view=COMPLETE&httpAccept=application/json&apiKey=dc1c396604f71b360feeecd6f767e1d4")
    data = json.loads(url.text)
    extractAbstracts(int(numOfPages))
    
    userInput = input("Continue? Press 'A' to quit: ")
    abstracts.close








