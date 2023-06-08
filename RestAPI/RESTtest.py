import requests
import json
    
url = requests.get("https://api.crossref.org/works?filter=has-abstract:true&mailto=mosesa3@vcu.edu").json()
# works?filter=has-abstract:true
dump = open("RestApiDump.txt", 'w') # unnecessary
dump.write(str(url))  # unnecessary

abstracts = open("restAPIabstracts.txt", "w")

def extractAbstracts():
    abstracts = open("restAPIabstracts.txt", "a")
    for i in range(20):
        if url['message']['items'][i]['abstract'].__contains__("the"):
            abstract = url['message']['items'][i]['abstract'] + "\n"  # \n isn't required
            abstracts.writelines(abstract)
            print(abstract)
    abstracts.close

extractAbstracts()





