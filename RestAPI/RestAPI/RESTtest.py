import requests
import json
import re
## url = requests.get("https://api.crossref.org/works?query= " + searchTopic + " &rows=" + numOfJournals + "&filter=has-abstract:true&mailto=mosesa3@vcu.edu")
url = requests.get("https://api.crossref.org/works?query=%22polymer%22&rows=300&offset=1&filter=has-abstract:true&mailto=mosesa3@vcu.edu")
url = json.loads(url.text)
# works?filter=has-abstract:true

abstracts = open("RestAPI/restAPIabstracts.txt", "w")

def RESTAPIJSON(offset, ceiling, searchTopic):
    url = requests.get("https://api.crossref.org/works?query= " + searchTopic 
    + " &rows=" + str(ceiling) + "&offset=" + str(offset) + "&filter=has-abstract:true&mailto=mosesa3@vcu.edu")
    return json.loads(url.text)

def extractAbstracts():
    abstracts = open("RestAPI/restAPIabstracts.txt", "a")
    RESTAPIExtraction(999, "kidney OR (renal AND tissue)")
            
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
    count = 0
    for i in range(ceiling):
        abstract = data['message']['items'][i]['abstract']
        abstract = re.sub("<\S+>", "", abstract)
        abstract = re.sub("[a-z]*&\S*;", "", abstract)
        abstract = re.sub("\s{2,}", "", abstract)
        abstracts.write(abstract)
        count += 1
    print(count)
    abstracts.close

extractAbstracts()





