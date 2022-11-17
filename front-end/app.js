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

            let name = document.getElementById('name');
            name.innerHTML = `<b>Name: </b>${userData.name}`;

    
            document.getElementById('user').innerHTML = userData.login;
            document.getElementById('location').innerHTML = userData.location;
            document.getElementById('company').innerHTML = userData.company;
            document.getElementById('followers').innerHTML = userData.followers;
            document.getElementById('following').innerHTML = userData.following;
            document.getElementById('public_repos').innerHTML = userData.public_repos;
            // document.getElementById('name').innerHTML = userData.name;
            let img = document.getElementById('img')
            img.src = userData.avatar_url;
        }