const express = require('express');
const bodyParser = require('body-parser');
const MongoClient = require('mongodb').MongoClient;
const cors = require('cors');
const app = express();
app.use(cors());
const port = 3000;
const uri = 'mongodb://127.0.0.1:27017/'

const client = new MongoClient(uri);
const database = client.db("transfermarkt");
const players = database.collection("players");

function getPlayer(query){
    return players.find(query).toArray();
}

function getRandomPlayer(){
    return players.aggregate([{ $match : { "2022" : {$in : [720, 294, 336, 1075] }}}, {$sample: {size:1}}]).toArray();
    //return players.aggregate([{$sample: {size:1}}]).toArray();
}

function getAllPlayers(){
    return players.find( {}, { projection: { ['name']: 1, _id: 0 } } ).toArray();
}

app.get('/players', async function(req, res){

    console.log('/players');
    var players = await getAllPlayers();
    var list = players.map(doc => doc['name']);
    
    res.send(list);

});

app.get('/input', async function(req, res){

    console.log('/input');
    var name = req.headers.name;
    var idBefore = parseInt(req.headers.idbefore);
    var query = {name:name};
    var player = await getPlayer(query);
    player = player[0];
    query = {id:idBefore};
    var playerBefore = await getPlayer(query);
    playerBefore = playerBefore[0];

    var teammates = false;

    for(var key in player){
        if(playerBefore[key] != undefined){
            if(player[key] == playerBefore[key]){
                teammates = true;
                break;
            }
        }
    }

    player.teammates = teammates;

    res.send(player);
});

app.get('/player/start', async function(req, res){

    console.log('/player/start');
    var playerStart = await getRandomPlayer();

    res.send(playerStart[0]);

});

app.get('/player/end', async function(req, res){

    console.log('/player/end');
    var playerEnd = await getRandomPlayer();

    res.send(playerEnd[0]);

});

app.get('/end', async function(req, res){

    console.log('/end');
    var idCurrent = parseInt(req.headers.idcurrent);
    var idEnd = parseInt(req.headers.playerend);
    var query = {id:idCurrent};
    var player = await getPlayer(query);
    player = player[0];
    query = {id:idEnd};
    var playerEnd = await getPlayer(query);
    playerEnd = playerEnd[0];

    var teammates = false;

    for(var key in player){
        if(playerEnd[key] != undefined){
            if(player[key] == playerEnd[key]){
                teammates = true;
                break;
            }
        }
    }

    res.send(teammates);

});

app.listen(port, () => {
    console.log('Server is running on port ' + port + '!');
});