import json
import requests

def retrieveLanguages(username, repoData):
    # responseRepo = requests.get("https://api.github.com/users/" + username + "/repos")
    # repoData = responseRepo.json()
    linesOfCodeDict = {}
    languageCounterDict = {}
    for i in repoData:
        repo = i['name']
        response = (requests.get("https://api.github.com/repos/{}/{}/languages".format(username, repo)))
        languageData = json.loads(response.text)
        for k, v in languageData.items():
            try:
                if k == {}: continue
                countBefore = int(languageCounterDict[k])
                before = int(linesOfCodeDict[k])
                countAfter = 1 + countBefore
                languageCounterDict[k] = str(countAfter)
                result = int(v) + before
                linesOfCodeDict[k] = str(result)
            except:
                languageCounterDict[k] = 1
                linesOfCodeDict[k] = v
    #languageDict has language Keys, but will have modified values for languages, with the first value containing lines
    #of code written for that language. Then seperated with a comma there is the amount of times this language was utilised by the user
    #in all their public repos e.g. 'Java' : '5000,2'
    languageDict = {}
    for k, v in linesOfCodeDict.items():
        languageDict[k] = "" + str(v) + "," + str(languageCounterDict[k])
    return languageDict
