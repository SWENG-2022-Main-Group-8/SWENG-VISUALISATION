function handleInput() {
    var user = document.getElementById("user").value;
    main(user);
}

async function getRequest(url) {
    const response = await fetch(url);
    let data = await response.json();
    return data;
}

async function main(user) {
    let url = `https://api.github.com/users/${user}/repos`;
    let repo = await getRequest(url).catch(error => console.error(error));

    console.log(repo)
}
