from flask import Flask, request, redirect, render_template, jsonify
from flask import session as current_session
import requests
import flask
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

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/menu')
def index():
    return render_template("index.html")

@app.route('/results', methods=["GET"])
def results_page():
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

        #dateRequired = datetime.strptime((requiredDay + "/" + requiredMonth + "/" + requiredYear), '%d/%m/%Y')
        dateRequired1 = datetime.now().strftime('%d/%m/%Y')
        print(dateRequired1)
        dateRequired = datetime.strptime(dateRequired1, '%d/%m/%Y')
        print(dateRequired.date())
        weekBefore = dateRequired.date() - timedelta(days=7)
        commitDict[weekBefore.strftime('%d/%m/%Y')] = 0
        for i in range(3):
            weekBefore = weekBefore - timedelta(days=7)
            commitDict[weekBefore.strftime('%d/%m/%Y')] = 0

        commitsInTotal = 0
        for i in user_repos:
            repo = i['name']
            try:
                commits_url = f'https://api.github.com/repos/{username}/{repo}/commits?per_page=100'
                response = (requests.get(commits_url, auth=('access_token', current_session['access_token'])))
            except requests.exceptions.RequestException as e: continue
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
                    print(currentWeek.date())
                    print(currentDate.date())

                    weekAfter = currentWeek.date() + timedelta(days=7)
                    print(weekAfter)
                    if((currentDate.date() == dateRequired1 and weekAfter == currentDate.date()) or currentWeek.date() <= currentDate.date() < weekAfter) :
                        print("S")
                        v = v + 1
                        commitDict[k] = v
            print(commitDict)
        #Get user events
        if 'username' not in request.args:
            events_url = f'https://api.github.com/users/{username}/events'
        user_events = requests.get(events_url, auth=('access_token', current_session['access_token']))
        user_events = user_events.json()

        #Get user location coords
        map_data = mapAPI.getLatLng(userData['location'])

        #Get user repos commit history
        repo_commits = []
        for repo in user_repos:
                repo_name = repo['name']
                commit_history_url = f'https://api.github.com/repos/{username}/{repo_name}/stats/participation'
                commit_history = requests.get(commit_history_url, auth=('access_token', current_session['access_token']))
                commit_history = commit_history.json()
                if 'message' not in commit_history:
                    this_repos_commits = {'name': repo_name, 'commits': commit_history['owner']}
                    repo_commits.append(this_repos_commits)
        
        repo_commits.sort(key=lambda x: sum(x['commits']), reverse=True)
        # print(repo_commits)

        try:
            return render_template("results2.html", userData=userData, user_repos=user_repos, language_dict=language_dict, map_data=map_data, user_events=user_events, repo_commits=repo_commits, commits_dict=commitDict)
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
        
if __name__ == "__main__":
    app.secret_key = "super_duper_secret_key"
    app.run(debug=True)


#maps api key - AIzaSyCaN_NjULWKTMBVQYhQMCHoUIcJvg3fQUk