var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function sendDataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        const userData = JSON.parse(xhr.responseText)

        getUserInfo(userData);
        
        if (chart1 != null) chart1.destroy();
        main(dataToSend);
    }
}

function sendData() {
    dataToSend = document.getElementById('data-input').value;
    if (!dataToSend) {
        console.log("Data is empty.");
        return;
    }
    console.log("Sending data: " + dataToSend);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "http://127.0.0.1:5000/username", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({ "data": dataToSend }));
}

async function getRequest(url) {
    const response = await fetch(url);
    let data = await response.json();
    return data;
}

async function main(user) {
    let url = `https://api.github.com/users/${user}/repos`;
    let repo = await getRequest(url)
    
    getLanguages(repo, user);

    console.log(repo)
}

function getUserInfo(userData) {

    let login = document.getElementById('user');
    login.innerHTML = `<b>Username: </b>${userData.login}`;

    let img = document.getElementById('img')
    img.src = userData.avatar_url;
    
    let name = document.getElementById('name');
    name.innerHTML = `<b>Name: </b>${userData.name == null ? 'Not specified' : userData.name}`;

    let company = document.getElementById('company');
    company.innerHTML = `<b>Company: </b>${userData.company == null ? 'Not specified' : userData.company}`;
    
    let location = document.getElementById('location');
    location.innerHTML = `<b>Location: </b>${userData.location == null ? 'Not specified' : userData.location}`;

    let followers = document.getElementById('followers');
    followers.innerHTML = `<b>Followers: </b>${userData.followers}`;

    let following = document.getElementById('following');
    following.innerHTML = `<b>Following: </b>${userData.following}`;

    let public_repos = document.getElementById('public_repos');
    public_repos.innerHTML = `<b>Public Repos: </b>${userData.public_repos}`;
}

async function getLanguages(repo, user) {
    let label = [];
    let data = [];
    let backgroundColor = [];

    for (i in repo) {
        let url = `https://api.github.com/repos/${user}/${repo[i].name}/languages`;
        let allLanguages = await getRequest(url)

        for (language in allLanguages) {

            if (label.includes(language)) {
                for (i = 0; i < label.length; i++)
                    if (language == label[i])
                        data[i] = data[i] + allLanguages[language];

            } else {
                label.push(language);
                data.push(allLanguages[language]);
                backgroundColor.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.5)`);
            }
        }

    }

    draw1('language', 'pie', 'languages', `User's languages (in bytes)`, label, data, backgroundColor);
}

function draw1(ctx, type, datasetLabel, titleText, label, data, backgroundColor) {

    let myChart = document.getElementById(ctx).getContext('2d');

    chart1 = new Chart(myChart, {
        type: type,
        data: {
            labels: label,
            datasets: [{
                label: datasetLabel,
                data: data,
                backgroundColor: backgroundColor,
                borderWidth: 1,
                borderColor: '#777',
                hoverBorderWidth: 2,
                hoverBorderColor: '#000'
            }],
        },
        options: {
            title: {
                display: true,
                text: titleText,
                fontSize: 20
            },
            legend: {
                display: true,
                position: 'bottom',
                labels: {
                    fontColor: '#000'
                }
            },
            layout: {
                padding: {
                    left: 50,
                    right: 0,
                    bottom: 0,
                    top: 0
                }
            },
            tooltips: {
                enabled: true
            }
        }
    });
}

var chart1 = null;

const handleOnMouseMove = e => {
    const {currentTarget: target} = e;

    const rect = target.getBoundingClientRect(),
        x = e.clientX - rect.left,
        y = e.clientY - rect.top;

    target.style.setProperty("--mouse-x", `${x}px`)
    target.style.setProperty("--mouse-y", `${y}px`)
}

for(const card of document.querySelectorAll(".card")){
    card.onmousemove = e => handleOnMouseMove(e);
}