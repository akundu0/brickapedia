// API key stuff
const apiKey = "90474b52a4291bd0d3ba0a85c7c9c323";
const setId = "75192-1"; // Example LEGO set ID

fetch(`https://rebrickable.com/api/v3/lego/sets/${setId}/`, {
    headers: { "Authorization": `key ${apiKey}` }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));

// fetch API lego set with number
function fetchLegoSet() {
    let setId = document.getElementById("set_id").value;
    fetch(`/api/get_set?set_id=${setId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error("Error:", error));
}

var button = document.getElementById("search_button");

button.addEventListener("click", function(){
    document.body.style.backgroundImage = "url('/static/assets/bg.png')";
});