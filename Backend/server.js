const express = require('express');
const bodyParser = require('body-parser');
const MongoClient = require('mongodb').MongoClient;
const app = express();
const port = 3000;
const uri = 'mongodb://127.0.0.1:27017/'

const client = new MongoClient(uri);
const database = client.db("transfermarkt");
const players = database.collection("players");

function getPlayer(query){
    return players.find(query).toArray();
}

function getRandomPlayer(){
    return players.aggregate([{$sample: {size: 1}}]).toArray();
}

app.get('/player', async function(req, res){

    var name = req.headers.name;
    var query = {name:name};
    var player = await getPlayer(query);

    res.send(player);
});

app.get('/start', async function(req, res){

    var playerStart = await getRandomPlayer();
    var playerEnd = await getRandomPlayer();

    res.send(playerStart[0].name + ', ' + playerEnd[0].name);

});

app.listen(port, () => {
    console.log('Server is running on port ' + port + '!');
});