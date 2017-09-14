// app.js

var path = require('path')
var config = require('read-config')(path.join(__dirname, 'config.json'))
var express = require('express')
var logger = require('morgan')
var session = require('express-session')({
  secret: config.session.secret,
  name: config.session.name,
  resave: true,
  saveUninitialized: false,
  unset: 'destroy'
})
var app = express()
var server = require('http').Server(app)
var myutil = require('./util')
var validator = require('validator')
var io = require('socket.io')(server, { serveClient: false })
var socket = require('./socket')
var expressOptions = require('./expressOptions')

// express
app.use(session)
app.use(myutil.basicAuth)
if (config.accesslog) app.use(logger('common'))
app.disable('x-powered-by')

// static files
app.use(express.static(path.join(__dirname, 'public'), expressOptions))

app.get('/ssh/host/:host?', function (req, res, next) {
  res.sendFile(path.join(path.join(__dirname, 'public', (config.useminified)
    ? 'client-min.htm' : 'client-full.htm')))
  // capture, assign, and validated variables
  req.session.ssh = {
    host: (validator.isIP(req.params.host + '') && req.params.host) ||
      (validator.isFQDN(req.params.host) && req.params.host) ||
      (/^(([a-z]|[A-Z]|[0-9]|[!^(){}\-_~])+)?\w$/.test(req.params.host) &&
      req.params.host) || config.ssh.host,
    port: (validator.isInt(req.query.port + '', {min: 1, max: 65535}) &&
      req.query.port) || config.ssh.port,
    header: {
      name: req.query.header || config.header.text,
      background: req.query.headerBackground || config.header.background
    },
    algorithms: config.algorithms,
    term: (/^(([a-z]|[A-Z]|[0-9]|[!^(){}\-_~])+)?\w$/.test(req.query.sshterm) &&
      req.query.sshterm) || config.ssh.term,
    allowreplay: validator.isBoolean(req.headers.allowreplay + '') || false,
    serverlog: {
      client: config.serverlog.client || false,
      server: config.serverlog.server || false
    },
    readyTimeout: (validator.isInt(req.query.readyTimeout + '', {min: 1, max: 300000}) &&
      req.query.readyTimeout) || config.ssh.readyTimeout
  }
  req.session.ssh.header.name && validator.escape(req.session.ssh.header.name)
  req.session.ssh.header.background &&
    validator.escape(req.session.ssh.header.background)
})

// express error handling
app.use(function (req, res, next) {
  res.status(404).send("Sorry can't find that!")
})

app.use(function (err, req, res, next) {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})

// socket.io
// expose express session with socket.request.session
io.use(function (socket, next) {
  (socket.request.res) ? session(socket.request, socket.request.res, next)
    : next()
})

// bring up socket
io.on('connection', socket)

module.exports = {server: server, config: config}
