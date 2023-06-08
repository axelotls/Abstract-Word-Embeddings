import json
import requests

# for example sake, abstracts.txt is cleared every time the code runs
# if the same topic is searched, there will be repeats
abstracts = open("SpringerNature/springerNatureAbstracts.txt", "w")


def extractAbstracts(numOfJournals, searchTopic):
    tempJournals = int(numOfJournals)
    offset = 1

    if (100 > tempJournals > 0):
        ceiling = tempJournals
        data = urlRequest(offset, ceiling)
        for i in range(0, tempJournals):
            if data['records'][i]['abstract'] != "":
                abstract = data['records'][i]['abstract'] + "\n"  # \n isn't required
                abstracts.writelines(abstract)
                print(abstract)

    else:
        ceiling = 100
        while (tempJournals > 0):
            data = urlRequest(offset, ceiling)
            for i in range(ceiling):
                i %= 100
                if data['records'][i]['abstract'] != "":
                    abstract = data['records'][i]['abstract'] + "\n"  # \n isn't required
                    abstracts.writelines(abstract)
                    print(abstract)

            offset += 100
            tempJournals -= 100

            if (tempJournals > 100):
                ceiling = 100
            else:
                ceiling = tempJournals

def urlRequest(offset, ceiling):
        url = requests.get("https://api.springernature.com/meta/v2/json?api_key=50fa5bb93bb66d04245858c6490c3293&q=" + 
        searchTopic + "&s=" + str(offset) + "&p=" + str(numOfJournals))
        return json.loads(url.text)

userInput = ""
while userInput != "A":
    abstracts = open("SpringerNature/springerNatureAbstracts.txt", "a")
    searchTopic = input("Enter a topic to search for: ")
    numOfJournals = input("Enter a number of pages to search through (max=100): ")
    extractAbstracts(numOfJournals, searchTopic)
    userInput = input("Continue? Press 'A' to quit: ")
    abstracts.close



