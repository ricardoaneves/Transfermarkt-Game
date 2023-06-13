const express = require('express');
const bodyParser = require('body-parser');
const MongoClient = require('mongodb').MongoClient;
const app = express();
const port = 3000;
const uri = 'mongodb://localhost:27017'

// Middleware
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

const client = new MongoClient(uri);

client.connect((error) => {

    if(error){
        console.error('Error connecting to MongoDB: ' + error);
        return;
    }
    console.log('Connected to MongoDB!');

    const db = client.db('transfermarkt');
    const collection = db.collection('players');

    app.listen(port, () => {
        console.log('Server is running on port ' + port + '!');
    });
});