var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

app.use(express.static('public'));
app.get('/', function (req, res) {
    res.sendfile(__dirname + '/public/index.html');
});

server.listen(2222);
// var server = app.listen(process.env.port || 8080, function () {
//   var port = server.address().port;
//   console.log('------------------------------------')
//   console.log('App is listening on port %s', port)
//   console.log('Press Ctrl+C to quit.')
//   console.log('------------------------------------')
// });

var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
   //host: 'https://search-twittmap-qtnxkqs26tfzc27letgg2blf5i.us-east-1.es.amazonaws.com:443'
    host: 'https://search-twittermap-hw-c3n4qckpkm4l3ald2i5conkdxy.us-west-2.es.amazonaws.com'
});

io.on('connection', function (socket) {
    socket.emit('news', {message: 'welcome!', id: socket.id});//Note that emit event name on the server matches the emit event name
    console.log('jin lai le');
    socket.on('my other event', function (data) {
        var key = data.key;
        console.log(key);//key word
        client.search({
            index: 'twitmap',
            fields: ['text','geo','user','time'],
            q: key,
            size: 1000
        }, function (error, body) {
            var result = [];
            console.log(body,'body');
            var hits = body.hits.hits;
            console.log(hits[0]);
            for (var i = 0; i < hits.length; i++) {
                //result[i] = hits[i]._source;
                result[i] = hits[i].fields;
            }
            console.log(result);
            var myObject = {
                "tweet": result
            };
            socket.emit('toggle', myObject);
        });
    });
});
