//Getting all the contributers for the React organisation
async function getReactContributorData(){
    let url = "https://api.github.com/repos/facebook/react/contributors";
    let reactContrib = await getRequest(url)

    print(reactContrib)
}

//Gets the json 
async function getRequest(url) {
    const response = await fetch(url);
    let data = await response.json();
    return data;
}

//Gets the data required for the map
function fillMapData(mapData) {
    let bool1 = mapData.longitude;
    let bool2 = mapData.latitude;
    console.log(bool1, bool2);
    if(bool1 && bool2){
        console.log("map initialize");
        // initialize map
        map = L.map('mapDiv').setView([mapData.latitude, mapData.longitude], 13);
        // set map tiles source
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            maxZoom: 18,
        }).addTo(map);
        // add marker to the map
        marker = L.marker([mapData.latitude, mapData.longitude]).addTo(map);
    }
}

//Gets the data for the languages graphs
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

//Used for get the language data and send it on the graph drawers
function languagesChart(language_info) {
    console.log(language_info)
    let label = [];
    let bytes = [];
    let repos = [];
    let backgroundColor = [];

    // for (let language in language_info) {
    //     label.push(language);
    //     data.push(language_info[language]);
    //     backgroundColor.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`);
    //
    // }

    for (let language in language_info) {
        const info = language_info[language].split(',',2);
        let bytesOfLanguages = info[0];
        let numberOfLanguages = info[1];

        label.push(language);
        bytes.push(bytesOfLanguages);
        repos.push(numberOfLanguages);
        backgroundColor.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`);
    }

    draw1('languagePie', 'pie', 'languages', `User's languages (in bytes)`, label, bytes, backgroundColor);

    draw2('languageBar', 'bar', 'languages', `Number of repos that use the language`, label, repos, backgroundColor);
}

//Creates the graph of top repos this year
function fillCommitChart(commitData) {
    const data = commitData['commits'];


    repoChart = new Chart(
        document.getElementById('repo_commits'),
        {
            type: 'bar',
            data: {
                labels: [...Array(52).keys()].map(i => i+1),
                datasets: [{
                    label: 'Commits by week',
                    data: data,
                    backgroundColor: generateColours(data)
                }]
            }
        }
    );
    
}

//Generate random colors for the graphs
function generateColours(list) {
    let coloursList = []
    for (item in list) {
        coloursList.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.8)`);
    }
    return coloursList;
}

//Creates a pie chart for language used by the person (in bytes)
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

//Creates the bar chart of number of repos that use a certain language
function draw2(ctx, type, datasetLabel, titleText, label, data, backgroundColor) {

    let myChart = document.getElementById(ctx).getContext('2d');

    chart2 = new Chart(myChart, {
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
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                display: false,
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
var chart2 = null;

//Hover effects for the menu page
document.getElementById("homeCards").onmousemove = e => {
    for(const card of document.getElementsByClassName("homeCard")){
        const rect = card.getBoundingClientRect(),
            x = e.clientX - rect.left,
            y = e.clientY - rect.top;

        card.style.setProperty("--mouse-x", `${x}px`)
        card.style.setProperty("--mouse-y", `${y}px`)
    }
}