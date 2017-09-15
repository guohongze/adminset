// socket/index.js

// private
var debug = require('debug')
var debugWebSSH2 = require('debug')('WebSSH2')
var SSH = require('ssh2').Client
var termCols, termRows

// public
module.exports = function socket (socket) {
  // if websocket connection arrives without an express session, kill it
  if (!socket.request.session) {
    socket.emit('401 UNAUTHORIZED')
    debugWebSSH2('SOCKET: No Express Session / REJECTED')
    socket.disconnect(true)
    return
  }
  var conn = new SSH()
  socket.on('geometry', function socketOnGeometry (cols, rows) {
    termCols = cols
    termRows = rows
  })
  conn.on('banner', function connOnBanner (data) {
        // need to convert to cr/lf for proper formatting
    data = data.replace(/\r?\n/g, '\r\n')
    socket.emit('data', data.toString('utf-8'))
  })

  conn.on('ready', function connOnReady () {
    console.log('WebSSH2 Login: user=' + socket.request.session.username + ' from=' + socket.handshake.address + ' host=' + socket.request.session.ssh.host + ' port=' + socket.request.session.ssh.port + ' sessionID=' + socket.request.sessionID + '/' + socket.id + ' allowreplay=' + socket.request.session.ssh.allowreplay + ' term=' + socket.request.session.ssh.term)
    socket.emit('title', 'ssh://' + socket.request.session.ssh.host)
    socket.request.session.ssh.header.background && socket.emit('headerBackground', socket.request.session.ssh.header.background)
    socket.request.session.ssh.header.name && socket.emit('header', socket.request.session.ssh.header.name)
    socket.emit('footer', 'ssh://' + socket.request.session.username + '@' + socket.request.session.ssh.host + ':' + socket.request.session.ssh.port)
    socket.emit('status', 'SSH CONNECTION ESTABLISHED')
    socket.emit('statusBackground', 'green')
    socket.emit('allowreplay', socket.request.session.ssh.allowreplay)
    conn.shell({
      term: socket.request.session.ssh.term,
      cols: termCols,
      rows: termRows
    }, function connShell (err, stream) {
      if (err) {
        SSHerror('EXEC ERROR' + err)
        conn.end()
        return
      }
      // poc to log commands from client
      if (socket.request.session.ssh.serverlog.client) var dataBuffer
      socket.on('data', function socketOnData (data) {
        stream.write(data)
        // poc to log commands from client
        if (socket.request.session.ssh.serverlog.client) {
          if (data === '\r') {
            console.log('serverlog.client: ' + socket.request.session.id + '/' + socket.id + ' host: ' + socket.request.session.ssh.host + ' command: ' + dataBuffer)
            dataBuffer = undefined
          } else {
            dataBuffer = (dataBuffer) ? dataBuffer + data : data
          }
        }
      })
      socket.on('control', function socketOnControl (controlData) {
        switch (controlData) {
          case 'replayCredentials':
            stream.write(socket.request.session.userpassword + '\n')
          /* falls through */
          default:
            console.log('controlData: ' + controlData)
        }
      })
      socket.on('disconnecting', function socketOnDisconnecting (reason) { debugWebSSH2('SOCKET DISCONNECTING: ' + reason) })
      socket.on('disconnect', function socketOnDisconnect (reason) {
        debugWebSSH2('SOCKET DISCONNECT: ' + reason)
        err = { message: reason }
        SSHerror('CLIENT SOCKET DISCONNECT', err)
        conn.end()
        // socket.request.session.destroy()
      })
      socket.on('error', function socketOnError (err) {
        SSHerror('SOCKET ERROR', err)
        conn.end()
      })

      stream.on('data', function streamOnData (data) { socket.emit('data', data.toString('utf-8')) })
      stream.on('close', function streamOnClose (code, signal) {
        err = { message: ((code || signal) ? (((code) ? 'CODE: ' + code : '') + ((code && signal) ? ' ' : '') + ((signal) ? 'SIGNAL: ' + signal : '')) : undefined) }
        SSHerror('STREAM CLOSE', err)
        conn.end()
      })
      stream.stderr.on('data', function streamStderrOnData (data) {
        console.log('STDERR: ' + data)
      })
    })
  })

  conn.on('end', function connOnEnd (err) { SSHerror('CONN END BY HOST', err) })
  conn.on('close', function connOnClose (err) { SSHerror('CONN CLOSE', err) })
  conn.on('error', function connOnError (err) { SSHerror('CONN ERROR', err) })
  conn.on('keyboard-interactive', function connOnKeyboardInteractive (name, instructions, instructionsLang, prompts, finish) {
    debugWebSSH2('conn.on(\'keyboard-interactive\')')
    finish([socket.request.session.userpassword])
  })
  if (socket.request.session.username && socket.request.session.userpassword && socket.request.session.ssh) {
    conn.connect({
      host: socket.request.session.ssh.host,
      port: socket.request.session.ssh.port,
      username: socket.request.session.username,
      password: socket.request.session.userpassword,
      tryKeyboard: true,
      algorithms: socket.request.session.ssh.algorithms,
      readyTimeout: socket.request.session.ssh.readyTimeout,
      debug: debug('ssh2')
    })
  } else {
    debugWebSSH2('Attempt to connect without session.username/password or session varialbles defined, potentially previously abandoned client session. disconnecting websocket client.\r\nHandshake information: \r\n  ' + JSON.stringify(socket.handshake))
    socket.emit('ssherror', 'WEBSOCKET ERROR - Refresh the browser and try again')
    socket.request.session.destroy()
    socket.disconnect(true)
  }

  /**
  * Error handling for various events. Outputs error to client, logs to
  * server, destroys session and disconnects socket.
  * @param {string} myFunc Function calling this function
  * @param {object} err    error object or error message
  */
  function SSHerror (myFunc, err) {
    var theError
    if (socket.request.session) {
      // we just want the first error of the session to pass to the client
      socket.request.session.error = (socket.request.session.error) || ((err) ? err.message : undefined)
      theError = (socket.request.session.error) ? ': ' + socket.request.session.error : ''
      // log unsuccessful login attempt
      if (err && (err.level === 'client-authentication')) {
        console.log('WebSSH2 ' + 'error: Authentication failure'.red.bold +
          ' user=' + socket.request.session.username.yellow.bold.underline +
          ' from=' + socket.handshake.address.yellow.bold.underline)
      } else {
        console.log('WebSSH2 Logout: user=' + socket.request.session.username + ' from=' + socket.handshake.address + ' host=' + socket.request.session.ssh.host + ' port=' + socket.request.session.ssh.port + ' sessionID=' + socket.request.sessionID + '/' + socket.id + ' allowreplay=' + socket.request.session.ssh.allowreplay + ' term=' + socket.request.session.ssh.term)
      }
      socket.emit('ssherror', 'SSH ' + myFunc + theError)
      socket.request.session.destroy()
      socket.disconnect(true)
    } else {
      theError = (err) ? ': ' + err.message : ''
      socket.disconnect(true)
    }
    debugWebSSH2('SSHerror ' + myFunc + theError)
  }
}
