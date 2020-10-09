/* Global Variables */
const API_KEY = "4848374c988d864089f78a7455ac9c05";
const BASE_URL = "http://api.openweathermap.org/data/2.5/weather?zip=";
// Create a new date instance dynamically with JS
let d = new Date();
let newDate = d.getMonth()+'.'+ d.getDate()+'.'+ d.getFullYear();

// Helper function to request the weather from openWeatherMap API using the country zipcode.
const getWeather = async (zipCode) => {
    const res = await fetch(BASE_URL + zipCode + "&APPID=" + API_KEY);

    try {
        const weather = await res.json();
        //console.log(weather);
        return weather;
    } catch(err) {
        console.log("error: " + err);
    }
}

// Helper function to make a post request for saving the data on server.
const saveData = async (path, data) => {

    const response = await fetch(path, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": 'application/json'
        },
        body: JSON.stringify(data)
    });

    try {
        const newData = await response.json();
        //console.log(newData);
        return newData;
    } catch(err) {
        console.log("Error: " + err);
    }
}

const updateUI = async () => {
    const request = await fetch('/data');
    try {
        const data = await request.json();
        //console.log(data);
        document.querySelector('#date').innerHTML = data.date;
        document.querySelector('#temp').innerHTML = data.temperature;
        document.querySelector('#content').innerHTML = data["user-input"];

    } catch(err) {
        console.log("Error: " + err);
    }

}

// Helper function for:
// - generating the weather.
// - save the data to our server.
// - update the UI with the current weather.
const generateWeather = () => {
    const zipCode = document.querySelector('#zip').value;
    const userInput = document.querySelector('#feelings').value;

    getWeather(zipCode)
    .then(function(data) {
        saveData('/', {temperature: data.weather[0].description, date: newDate, "user-input": userInput});
    }).then(updateUI);
}

// Click event listener to the generate button.
document.querySelector('#generate').addEventListener('click', generateWeather);