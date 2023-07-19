import requests
import json
import re

abstracts = open("Restabstracts.txt", "w")

def RESTAPIJSON(offset, ceiling, searchTopic):
    url = requests.get("https://api.crossref.org/works?query= " + searchTopic 
    + " &rows=" + str(ceiling) + "&offset=" + str(offset) + "&filter=has-abstract:true&mailto=mosesa3@vcu.edu")
    return json.loads(url.text)
            
def RESTAPIExtraction(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 0

    if (tempJournals <= 1000):
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
                continue
            else:
                RESTAPIExtraction(tempJournals, searchTopic)

def RESTAPIparser(ceiling, data):
    count = 0
    for i in range(ceiling):
        try:
            abstract = str(data['message']['items'][i]['abstract'])
            abstract = re.sub("<\S+>", "", abstract)
            abstract = re.sub("[a-z]*&\S*;", "", abstract)
            abstract = re.sub("\s{2,}", "", abstract)
            abstracts.write(abstract)
            count += 1
        except (TypeError) as error:
            break
    if count != 0:
        print(count)
    abstracts.close

searchTopic = input("Enter a topic: ")
numOfJournals = input("Enter a number of journals: ")

RESTAPIExtraction(numOfJournals, searchTopic)




