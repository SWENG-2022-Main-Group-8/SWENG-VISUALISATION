import json
import requests
from datetime import datetime, date, timedelta

# username = "ArshadMohammadTCD"
# requiredDay = '30'
# requiredMonth = '04'
# requiredYear = '2022'

def commitsLastFourWeeks(username, requiredDay, requiredMonth, requiredYear):
    commitDict = {}
    dateRequired = datetime.strptime((requiredDay + "/" + requiredMonth + "/" + requiredYear), '%d/%m/%Y')
    weekBefore = dateRequired.date() - timedelta(days=7)
    commitDict[weekBefore.strftime('%d/%m/%Y')] = 0
    for i in range(3):
        weekBefore = weekBefore - timedelta(days=7)
        commitDict[weekBefore.strftime('%d/%m/%Y')] = 0

    responseRepo = requests.get("https://api.github.com/users/" + username + "/repos")
    repoData = responseRepo.json()
    commitsInTotal = 0
    for i in repoData:
        repo = i['name']
        try:
            response = (requests.get("https://api.github.com/repos/{}/{}/commits?per_page=100".format(username,repo)))
        except requests.exceptions.RequestException as e:
            continue
        contributorData = json.loads(response.text)
        for i in contributorData:
            try:
                name = i['author']['login']
            except: continue # for error of i['author']['login'] not existing in certain cases and giving None
            if(name != username) : continue
            commitsInTotal = commitsInTotal + 1
            date = i['commit']['author']['date']
            year = date[0:4]
            month = date[5:7]
            day = date[8:10]
            currentDate = datetime.strptime((day + "/" + month + "/" + year), '%d/%m/%Y')
            for k,v in commitDict.items():
                currentWeek = datetime.strptime(k, '%d/%m/%Y')
                weekAfter = currentWeek.date() + timedelta(days=7)
                if(currentWeek.date() <= currentDate.date() <= weekAfter) :
                    v = v + 1
                    commitDict[k] = v

    print(commitDict)
    print(commitsInTotal)
    return commitDict