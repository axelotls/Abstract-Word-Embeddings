import requests
import json
import re
## url = requests.get("https://api.crossref.org/works?query= " + searchTopic + " &rows=" + numOfJournals + "&filter=has-abstract:true&mailto=mosesa3@vcu.edu")
url = requests.get("https://api.crossref.org/works?query=%22polymer%22&rows=300&offset=1&filter=has-abstract:true&mailto=mosesa3@vcu.edu")
url = json.loads(url.text)
# works?filter=has-abstract:true

abstracts = open("restAPIabstracts.txt", "w")

def extractAbstracts():
    abstracts = open("restAPIabstracts.txt", "a")
    for i in range(300):
        if url['message']['items'][i]['abstract'].__contains__("the"):
            abstract = url['message']['items'][i]['abstract'] + "\n"  # \n isn't required
            abstract = re.sub("<\S+>", "", abstract)
            abstract = re.sub("[a-z]*&\S*;", "", abstract)
            abstract = re.sub("\s{2,}", "", abstract)
            abstracts.write(abstract)
            print(abstract)
    abstracts.close

extractAbstracts()





