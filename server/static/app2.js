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
function insertionDeletionChart(insertionDeletionData) {
    console.log(insertionDeletionData)
    let label = [];
    let commitsData = [];
    let insertionsData = [];
    let deletionsData = [];

    let backgroundColor = [];
    for (let repo in insertionDeletionData) {
        const info = insertionDeletionData[repo].split(',',3);
        commitsData.push(info[0]);
        insertionsData.push(info[1]);
        deletionsData.push(info[2]);
        label.push(repo);
        backgroundColor.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`);
    }
    draw4('insertionsDeletions', 'bar', 'line', 'Additions, Deletions and Commits of Repositories', label, commitsData, insertionsData, deletionsData, backgroundColor);
}

function languagesChart(language_info) {
    console.log(language_info)
    let label = [];
    let bytes = [];
    let repos = [];
    let backgroundColor = [];

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
function contributionData(contributionDict) {
    console.log(contributionDict)
    let label = [];
    let contributionPercent = [];
    let totalCommits = [];
    let backgroundColor = [];

    for (let repo in contributionDict) {
        const info = contributionDict[repo].split(',',2);
        let percentageContribution = info[0];
        let commitsTotal = info[1];

        label.push(repo);
        contributionPercent.push(percentageContribution);
        totalCommits.push(commitsTotal);
        backgroundColor.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`);
    }
}
function commitsGraph(commitsData) {
    console.log(commitsData)
    let label = [];
    let commits = [];
    let backgroundColor = [];
    console.log(commitsData)

    const orderedDates = {};
    Object.keys(commitsData).sort(function(a, b) {
        return a.split('/').reverse().join('').localeCompare(b.split('/').reverse().join(''));
    }).forEach(function(key) {
        orderedDates[key] = commitsData[key];
    })

    console.log(orderedDates);

    for (let date in orderedDates) {
        label.push(date);
        commits.push(commitsData[date]);
        console.log(date +" " + commitsData[date])
        backgroundColor.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`);
    }
    draw3('commitBar', 'bar', 'commits', `Commit's in the past four weeks`, label, commits, backgroundColor);
}

//Creates the graph of top repos this year
function fillCommitChart(commitData) {
    const data = commitData['commits'];
    console.log(data)

    if(repoChart != null) {
        repoChart.destroy();
    }
    repoChart = new Chart(
        document.getElementById('repo_commits'),
        {
            type: 'line',
            data: {
                labels: [...Array(52).keys()].map(i => i+1),
                datasets: [{
                    label: 'Commits by week',
                    data: data,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
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
function draw3(ctx, type, datasetLabel, titleText, label, data, backgroundColor) {

    let myChart = document.getElementById(ctx).getContext('2d');
    chart3 = new Chart(myChart, {
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
            elements: {
                bar: {
                    borderWidth: 2,
                }
            },
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
                // position: 'right',
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
function draw4(ctx, type, type2, titleText, label, commits, insertions, deletions, backgroundColor) {
    let myChart = document.getElementById(ctx).getContext('2d');
    chart4 = new Chart(myChart, {
        type: type,
        data: {
            labels: label,
            datasets: [{
                type : type2,
                label: 'commits',
                data: commits,
                // backgroundColor: backgroundColor,
                borderWidth: 1,
                borderColor: 'rgba(0, 0, 255, 0.2)',
                hoverBorderWidth: 2,
                fill: false,
                hoverBorderColor: '#000',
                yAxisID: 'y-axis-2',
            }, {
                yAxisID: 'y-axis-1',
                type : type,
                label: 'insertions',
                data: insertions,
                backgroundColor: 'rgba(0, 255, 0, 0.2)',
                borderWidth: 1,
                hoverBorderWidth: 2,
                hoverBorderColor: '#000',
            },
            {
                type : type,
                label: 'deletions',
                data: deletions,
                backgroundColor: 'rgba(255, 0, 0, 0.2)',
                borderColor: 'white',
                borderWidth: 1,
                hoverBorderWidth: 2,
                hoverBorderColor: '#000',
                yAxisID: 'y-axis-1'
            }]
        },
        options: {
            responsive : true,
            title: {
                display: true,
                text: titleText,
                fontSize: 20
            },
            legend: {
                display: true,
                position: 'top',
                labels: {
                    fontColor: '#000'
                }
            },
            tooltips: {
                mode : 'index',
                enabled: true,
                intersect : true
            },
            scales: {
                yAxes: [{
                    ticks: {
                        // display: true,
                        // stacked: true,
                        // stepSize: 20,
                        // min: minimu,
                        // max: maximu
                    },
                    type: 'linear',
                    display: true,
                    position: 'left',
                    id: 'y-axis-1',
                },
                    {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    id: 'y-axis-2',
                    gridLines: {
                        drawOnChartArea: false,
                    },
                }
                ]
            },
        }

    });
}
var chart1 = null;
var chart2 = null;
var chart3 = null;
var chart4 = null;
var repoChart = null;

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
