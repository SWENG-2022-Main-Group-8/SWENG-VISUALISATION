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
    }
}

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        dataDiv = document.getElementById('result-container');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}

function getUsers() {
    console.log("Get users...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "http://127.0.0.1:5000/username", true);
    // Send the request over the network
    xhr.send(null);
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