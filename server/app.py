import sys
from flask import Flask, request, redirect, render_template, jsonify
from flask import session as current_session
import requests
import flask
import httpx
import asyncio
from library import username as usernameAPI
from library import individualMap as mapAPI
from library import languageData as languagesAPI
from library import commitData as commitAPI
from library import org_maps as orgMapAPI
from flask_cors import CORS
from datetime import datetime, date, timedelta
import json
import os


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
CORS(app)
client_id = app.config.get("CLIENT_ID")
client_secret = app.config.get("CLIENT_SECRET")
app.secret_key = "super_duper_secret_key2"

async def get_user_commit_data(session, username, repo_name):
    commit_history_url = f'https://api.github.com/repos/{username}/{repo_name}/stats/participation'
    at = current_session['access_token']
    commit_history = (await session.get(commit_history_url, auth=('access_token', at))) # dont wait for the response of API
    return commit_history.json()

# function converted to coroutine
async def get_user_commit_data_for_all_repos(username, repo_names):
    async with httpx.AsyncClient() as session: # async client used for async functions
        tasks = [get_user_commit_data(session,username,repo_name) for repo_name in repo_names]        
        result = await asyncio.gather(*tasks, return_exceptions=True) # gather used to collect all coroutines and run them using loop and get the ordered response
    return result

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/menu')
def index():
    return render_template("index.html")

@app.route('/results', methods=["GET"])
async def results_page():
    if request.method == 'GET':
        repos_url = 'https://api.github.com/user/repos'
        access_token_url = 'https://api.github.com/user'
        events_url = ''

        #User is searching for another user
        if 'username' in request.args:
            username = request.args['username']
            access_token_url = f'https://api.github.com/users/{username}'
            repos_url = f'https://api.github.com/users/{username}/repos'
            events_url = f'https://api.github.com/users/{username}/events'

        #User is not logged in
        if 'access_token' not in current_session:
            return redirect('/login')

        #User is logged in
        # Get logged in user information from github api
        userData = requests.get(access_token_url, auth=('access_token', current_session['access_token']))
        userData = userData.json()
        username = userData['login']

        #Get logged in user repos
        user_repos = requests.get(repos_url, auth=('access_token', current_session['access_token']))
        user_repos = user_repos.json()

        #Get languages(bytes of code, number of times used)
        language_dict = {}
        linesOfCodeDict = {}
        languageCounterDict = {}
        for i in user_repos:
            repo = i['name']
            language_url = f'https://api.github.com/repos/{username}/{repo}/languages'
            response = (requests.get(language_url, auth=('access_token', current_session['access_token'])))
            languageData = json.loads(response.text)
            for k, v in languageData.items():
                try:
                    if k == {} or k == 'message' or k == 'documentation_url':
                        continue
                    countBefore = int(languageCounterDict[k])
                    before = int(linesOfCodeDict[k])
                    countAfter = 1 + countBefore
                    languageCounterDict[k] = str(countAfter)
                    result = int(v) + before
                    linesOfCodeDict[k] = str(result)
                except:
                    languageCounterDict[k] = 1
                    linesOfCodeDict[k] = v
        for k, v in linesOfCodeDict.items():
            language_dict[k] = "" + str(v) + "," + str(languageCounterDict[k])

        #Get number of commits from past four weeks till today
        commitDict = {}
        contributionDict = {}
        dateRequired = datetime.strptime(("25" + "/" + "10" + "/" + "2022"), '%d/%m/%Y')
        # dateRequired1 = datetime.now().strftime('%d/%m/%Y')
        # dateRequired = datetime.strptime(dateRequired1, '%d/%m/%Y')
        weekBefore = dateRequired.date() - timedelta(days=7)
        commitDict[weekBefore.strftime('%d/%m/%Y')] = 0
        for i in range(3):
            weekBefore = weekBefore - timedelta(days=7)
            commitDict[weekBefore.strftime('%d/%m/%Y')] = 0

        print(commitDict)
        commitsInTotal = 0
        for i in user_repos:
            repo = i['name']
            commitsByUser = 0
            commitsInRepo = 0
            try:
                commits_url = f'https://api.github.com/repos/{username}/{repo}/commits?per_page=100'
                response = (requests.get(commits_url, auth=('access_token', current_session['access_token'])))
            except requests.exceptions.RequestException as e: continue
            contributorData = json.loads(response.text)
            for i in contributorData:
                try:
                    name = i['author']['login']
                except: continue # for error of i['author']['login'] not existing in certain cases and giving None
                if(name != username) :
                    commitsInRepo = commitsInRepo + 1
                    continue
                commitsInRepo = commitsInRepo + 1
                commitsByUser = commitsByUser + 1
                commitsInTotal = commitsInTotal + 1
                date = i['commit']['author']['date']
                year = date[0:4]
                month = date[5:7]
                day = date[8:10]
                currentDate = datetime.strptime((day + "/" + month + "/" + year), '%d/%m/%Y')
                for k,v in commitDict.items():
                    currentWeek = datetime.strptime(k, '%d/%m/%Y')
                    weekAfter = currentWeek.date() + timedelta(days=7)
                    if((currentDate.date() == dateRequired.date() and weekAfter == currentDate.date()) or currentWeek.date() <= currentDate.date() < weekAfter) :
                        v = v + 1
                        commitDict[k] = v
            if(commitsInRepo == 0): continue
            contribution = (commitsByUser/commitsInRepo) * 100
            contributionDict[repo] = str(contribution) + "%"
        print(commitDict)

        #Getting number of commits, insertions, deletions from repos
        commitInsertionDeletionDict = {}
        for i in user_repos:
            repo = i['name']
            commits = 0
            insertions = 0
            deletions = 0
            # try:
            insertions_url = "https://api.github.com/repos/{}/{}/stats/contributors".format(username, repo)
            response = (requests.get(insertions_url, auth=('access_token', current_session['access_token'])))
            # except requests.exceptions.RequestException as e: continue
            stats = json.loads(response.text)
            for stat in stats:
                try:
                    name = stat['author']['login']
                except: continue # for error of i['author']['login'] not existing in certain cases and giving None
                if name == username:
                    commits = stat['total'];
                    for ad in stat['weeks']:
                        insertions = insertions + ad['a']
                        deletions = deletions + ad['d']
<<<<<<< Updated upstream
            if commits == 0 : continue
=======
            #         print(commits)
            #         print(insertions)
            #         print(deletions)
            # print(str(insertions) + " " + str(deletions) + " " + str(commits))
            # if commits == 0 : continue
>>>>>>> Stashed changes
            deletions = deletions * -1
            commitInsertionDeletionDict[repo] = str(commits) + "," + str(insertions) + "," + str(deletions)
        # print(commitInsertionDeletionDict)


        #Get user events
        if 'username' not in request.args:
            events_url = f'https://api.github.com/users/{username}/events'
        user_events = requests.get(events_url, auth=('access_token', current_session['access_token']))
        user_events = user_events.json()

        #Get user location coords
        map_data = mapAPI.getLatLng(userData['location'])


        #Get user repos commit history
        repo_commits_final = []
        repo_names = [repo['name'] for repo in user_repos]
        repo_commits = await get_user_commit_data_for_all_repos(username, repo_names)
        print(repo_commits)
        for i in range(len(repo_commits)):
            if 'message' not in repo_commits[i]:
                this_repos_commits = {'name': user_repos[i]['full_name'], 'commits': repo_commits[i]['owner']}
                repo_commits_final.append(this_repos_commits)
        
        repo_commits_final.sort(key=lambda x: sum(x['commits']), reverse=True)
        

        try:
            return render_template("results2.html", userData=userData, user_repos=user_repos, language_dict=language_dict, map_data=map_data, user_events=user_events, repo_commits=repo_commits, commits_dict=commitDict, insertionDeletion_dict=commitInsertionDeletionDict)

        except AttributeError:
            app.logger.debug('error getting username from github, whoops')
            return "I don't know who you are; I should, but regretfully I don't", 500

@app.route('/map')
def map_page():
    return render_template("map.html")

@app.route('/handlegithublogin')
def handle_github_login():
    fetch_url = 'https://github.com/login/oauth/authorize' + \
                '?client_id=' + client_id + \
                '&scope=user%20repo%20public_repo' + \
                '&allow_signup=true'
    #print fetch_url
    return redirect(fetch_url)

@app.route('/github-callback', methods=['GET', 'POST'])
def handle_github_callback():
    if 'code' in request.args:
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': request.args['code']
        }
        headers = {'Accept': 'application/json'}
        req = requests.post('https://github.com/login/oauth/access_token', params=params, headers=headers)
        resp = req.json()

        if 'access_token' in resp:
            current_session['access_token'] = resp['access_token']
            return redirect("/menu")
        else:
            return jsonify(error="Error retrieving access_token"), 404
    else:
        return jsonify(error="404_no_code"), 404

@app.route('/hellotest')
def hello_test():
    return 'Hello world!'

@app.route('/username', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")

    if request.method == "GET":
        languages = languagesAPI.retrieveLanguages("OmaidQ")
        commitHistory = commitAPI.commitsLastFourWeeks("ArshadMohammadTCD", "19", "11", "2022")
        with open("OmaidQ.json", "r") as f:
            data = json.load(f)
            merge = dict(data.items() | languages.items() | commitHistory.items())
            return flask.jsonify(merge)

    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        username = received_data['data']
        userInfo = usernameAPI.userInfo(username)
        languages = languagesAPI.retrieveLanguages(username)
        print("---------------------")
        coords = mapAPI.getLatLng(data.get("location"))
        data = mapAPI.mergeDictionary(data, coords)
        print(data)
        mergeOfDataAndLanguages = dict(userInfo.items() | languages.items())
        return flask.Response(response=json.dumps(mergeOfDataAndLanguages), status=201)
        
@app.route('/react', methods=["GET"])
def react():
    try:
        url = "https://api.github.com/repos/facebook/react/contributors?per_page=100"
        response =  requests.get(url)
        print(json.loads(response.text))
        return json.loads(response.text)

    except:
        print("Error")
        return '{}'
        data = bk.re_to_json(username)
        return Flask.Response(response=json.dumps(data), status=201)

@app.route('/organisation-map', methods=['POST'])
def organisationMaps():
     if request.method == "POST":
        received_data = request.get_json()
      
        print(f"received data: {received_data}")

        mapOrg = received_data['data']
        mapOrgData = orgMapAPI.getOrgLocationData(mapOrg)
        return flask.Response(response=json.dumps(mapOrgData), status=201)    

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)

#maps api key - AIzaSyCaN_NjULWKTMBVQYhQMCHoUIcJvg3fQUk