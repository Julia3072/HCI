var socketio = require('socket.io');
var serialport = require('serialport');
var SerialPort = serialport.SerialPort;
var portname = process.argv[2];
var shareData = "\n";
var myPort = new SerialPort(portname, { baudRate: 9600,
options: false,
parser: serialport.parsers.readline("\r\n")
});

myPort.on('open', function(){ console.log('port is open');});
myPort.on('close', function(){ console.log('port is closed'); });
myPort.on('error', function(){ console.log('some error - fix it'); });
myPort.on('data', function(data) {
shareData = data + "\n";
io.emit('news', { arduino: shareData });
myPort.write('1'); // establish connection with arduino example
});
// server
var app = require('http').createServer(handler);
var io = require('socket.io')(app);
var fs = require('fs');
app.listen(3001);
function handler (req, res) { fs.readFile(__dirname + '/index.html', function (err, data) {
if (err) {
res.writeHead(500);
return res.end('Error loading index.html');
} res.writeHead(200); res.end(data);
}); }
io.on('connection', function (socket) { socket.emit('news', { arduino: shareData }); socket.on('my other event', function (data) {
console.log(data); });
       });
