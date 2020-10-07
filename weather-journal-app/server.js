// Setup empty JS object to act as endpoint for all routes
projectData = {};

// Require Express to run server and routes
const express = require('express');
const bodyParser = require('body-parser');
// Start up an instance of app
const app = express();
/* Middleware*/
//Here we are configuring express to use body-parser as middle-ware.
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Cors for cross origin allowance

// Initialize the main project folder
app.use(express.static('website'));


// Setup Server
const PORT = 8000;

app.listen(PORT,() => {
    console.log('Listening to port: ' + PORT);
});

// GET route
app.get('/', (req, res) => {
    res.send(projectData);
});

// POST route
app.post('/', (req, res) => {
    projectData = {
        temprature: req.body.temperature,
        date: req.body.date,
        "user-response": req.body["user-response"]
    }
});