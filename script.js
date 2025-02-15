const apiKey = "90474b52a4291bd0d3ba0a85c7c9c323";
const setId = "75192-1"; // Example LEGO set ID

fetch(`https://rebrickable.com/api/v3/lego/sets/${setId}/`, {
    headers: { "Authorization": `key ${apiKey}` }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));
