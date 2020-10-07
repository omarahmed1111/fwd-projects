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
        console.log(weather);
        return weather;
    } catch(err) {
        console.log("error: " + err);
    }
}

// Helper function for:
// - generating the weather.
// - save the data to our server.
// - update the UI with the current weather.
const generateWeather = () => {
    const zipCode = document.querySelector('#zip').value;
    const weather = getWeather(zipCode);
}

// Click event listener to the generate button.
document.querySelector('#generate').addEventListener('click', generateWeather);