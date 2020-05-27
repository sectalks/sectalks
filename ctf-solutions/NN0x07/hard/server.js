
const DEFAULT_INDEX = 'index.html';

const HTTP_STATUS_OK = 200;
const HTTP_STATUS_PARTIAL_CONTENT = 206;
const HTTP_STATUS_NOT_MODIFIED = 304;
const HTTP_STATUS_ERR = 500;
const HTTP_STATUS_BAD_REQUEST = 400;
const HTTP_STATUS_FORBIDDEN = 403;
const HTTP_STATUS_NOT_FOUND = 404;
const HTTP_STATUS_INVALID_METHOD = 405;
const HTTP_STATUS_REQUEST_RANGE_NOT_SATISFIABLE = 416;

const VALID_HTTP_METHODS = ['GET', 'HEAD', 'POST', 'OPTIONS'];

const RANGE_REQUEST_HEADER_TEST = /^bytes=/;
const RANGE_REQUEST_HEADER_PATTERN = /\d*-\d*/g;

const TIME_MS_PRECISION = 3;

const MULTIPART_SEPARATOR = '--MULTIPARTSEPERATORaufielqbghgzwr';

const NEWLINE = '\n';


var EventEmitter = require('events').EventEmitter;
var util         = require('util');
var http         = require('http');
var url          = require('url');
var mime         = require('mime');
var path         = require('path');
var fs           = require('fs');
var opn          = require('opn');
var slice        = Array.prototype.slice;


/**
Exposes the StaticServer class
*/
module.exports = StaticServer;


/**
Create a new instance of StaticServer class

Options are :
   - name          the server name, what will be sent as "X-Powered-by"
   - host          the host interface where the server will listen to. If not specified,
                   the server will listen on any networking interfaces
   - cors          a cors header, will be sent as "Access-Control-Allow-Origin",
   - port          the listening port number
   - rootPath      the serving root path. Any file above that path will be denied
   - followSymlink true to follow any symbolic link, false to forbid
   - templates
      - index      the default index file to server for a directory (default 'index.html')
      - notFound   the 404 error template
   - noCache       disables 304 responses
   - open          open server in the local browser

@param options {Object}
*/
function StaticServer(options) {
  options = options || {};

  if (!options.rootPath) {
    throw new Error('Root path not specified');
  }

  if(!options.templates){
    options.templates = {};
  }

  this.name = options.name;
  this.host = options.host;
  this.port = options.port;
  this.cors = options.cors;
  this.rootPath = path.resolve(options.rootPath);
  this.followSymlink = !!options.followSymlink;
  this.templates = {
    'index': (options.templates.index || DEFAULT_INDEX),
    'notFound': options.templates.notFound
  };
  // the arguments parser converts `--no-XXXX` to `XXXX` with a value of false;
  this.noCache = !options.cache;
  this.open = options.open

  if (options.index) {
    console.log("options.index is now deprecated please use options.templates.index instead.");
    this.templates.index = options.index;
  }

  Object.defineProperty(this, '_socket', {
    configurable: true,
    enumerable: false,
    writable: true,
    value: null
  });

}
util.inherits(StaticServer, EventEmitter);

/**
Expose the http.STATUS_CODES object
*/
StaticServer.STATUS_CODES = http.STATUS_CODES;


/**
Start listening on the given host:port

@param callback {Function}    the function to call once the server is ready
*/
StaticServer.prototype.start = function start(callback) {
  this._socket = http.createServer(requestHandler(this)).listen(this.port, this.host, callback);
  if(this.open && this.port){
    opn('http://localhost:' + this.port);
  }
}


/**
Stop listening
*/
StaticServer.prototype.stop = function stop() {
  if (this._socket) {
    this._socket.close();
    this._socket = null;
  }
}


/**
Return the server's request handler function

@param server {StaticServer}  server instance
@return {Function}
*/
function requestHandler(server) {
  return function handler(req, res) {
    var uri = req.path = decodeURIComponent(url.parse(req.url).pathname);
    var filename = path.join(server.rootPath, uri);
    var timestamp = process.hrtime();

    // add a property to get the elapsed time since the request was issued
    Object.defineProperty(req, 'elapsedTime', {
      get: function getElapsedTime() {
        var elapsed = process.hrtime(timestamp);
        return (elapsed[0] ? elapsed[0] + 's ' : '') + (elapsed[1] / 1000000).toFixed(TIME_MS_PRECISION) + 'ms';
      }
    });

    res.headers = {};
    if (server.name) {
      res.headers['X-Powered-By'] = server.name;
    }

    if (server.cors) {
      res.headers['Access-Control-Allow-Origin'] = server.cors;
    }

    server.emit('request', req, res);

    if (VALID_HTTP_METHODS.indexOf(req.method) === -1) {
      return sendError(server, req, res, null, HTTP_STATUS_INVALID_METHOD);
    } else if (!validPath(server.rootPath, filename)) {
      return sendError(server, req, res, null, HTTP_STATUS_FORBIDDEN);
    }

    getFileStats(server, [filename, path.join(filename, server.templates.index)], function (err, stat, file, index) {
      if (err) {
        handleError(server, req, res, err);
      } else if (stat.isDirectory()) {
        //
        // TODO : handle directory listing here
        //
        sendError(server, req, res, null, HTTP_STATUS_FORBIDDEN);
      } else {
        sendFile(server, req, res, stat, file);
      }
    });
  };
}


/**
Handle an error

Currently assumes that the only error would be a 404 error.

@param server {StaticServer} server instance
@param req {Object} request Object
@param res {Object} response Object
@param err {Object} the error to handle
*/
function handleError(server, req, res, err){
  if(server.templates.notFound){
    getFileStats(server, [server.templates.notFound], function(err, stat, file, index){
      if (err) {
        sendError(server, req, res, null, HTTP_STATUS_NOT_FOUND);
      } else {
        res.status = HTTP_STATUS_NOT_FOUND;
        sendFile(server, req, res, stat, file);
      }
    });
  }else{
    sendError(server, req, res, null, HTTP_STATUS_NOT_FOUND);
  }
}



/**
Check that path is valid so we don't access invalid resources

@param rootPath {String}    the server root path
@param file {String}        the path to validate
*/
function validPath(rootPath, file) {
  var resolvedPath = path.resolve(rootPath, file);

  // only if we are still in the rootPath of the static site
  return resolvedPath.indexOf(rootPath) === 0;
}


/**
Get stats for the given file(s). The function will return the stats for the
first valid (i.e. found) file or directory.

    getFile(server, ['file1', 'file2'], callback);

The callback function receives four arguments; an error if any, a stats object,
the file name matching the stats found, and the actual index of the file from
the provided list of files.

@param server {StaticServer}    the StaticServer instance
@param files {Array}            list of files
@param callback {Function}      a callback function
*/
function getFileStats(server, files, callback) {
  var dirFound;
  var dirStat;
  var dirIndex;

  function checkNext(err, index) {
    if (files.length) {
      next(files.shift(), index + 1);
    } else if (dirFound) {
      // if a directory was found at some point, return it and ignore the error
      callback(null, dirStat, dirFound, dirIndex);
    } else {
      callback(err || new Error('File not found'));
    }
  }

  function next(file, index) {
    fs.lstat(file, function (err, stat) {
      if (err) {
        checkNext(err, index);
      } else if (stat.isSymbolicLink()) {
        if (server.followSymlink) {
          fs.readlink(file, function (err, fileRef) {
            if (err) {
              checkNext(err, index);
            } else {
              if (!path.isAbsolute(fileRef)) {
                fileRef = path.join( path.dirname(file), fileRef );
              }
              server.emit('symbolicLink', fileRef);
              next(fileRef, index);
            }
          });
        } else {
          callback(new Error('Symbolic link not allowed'));
        }
      } else if (stat.isDirectory()) {
        if (!dirFound) {
          dirFound = file;
          dirStat = stat;
          dirIndex = index;
        }
        checkNext(null, index);
      } else {
        callback(null, stat, file, index);
      }
    });
  }

  checkNext(null, 0);
}


/**
Validate that this file is not client cached

@param req {Object}       the request object
@param res {Object}       the response object
@return {boolean}         true if the file is client cached
*/
function validateClientCache(server, req, res, stat) {
  var mtime         = stat.mtime.getTime();
  var clientETag  = req.headers['if-none-match'];
  var clientMTime = Date.parse(req.headers['if-modified-since']);

  if (server.noCache) return false;

  if ((clientMTime  || clientETag) &&
      (!clientETag  || clientETag === res.headers['Etag']) &&
      (!clientMTime || clientMTime >= mtime)) {

    // NOT MODIFIED responses should not contain entity headers
    [
      'Content-Encoding',
      'Content-Language',
      'Content-Length',
      'Content-Location',
      'Content-MD5',
      'Content-Range',
      'Content-Type',
      'Expires',
      'Last-Modified'
    ].forEach(function(entityHeader) {
        delete res.headers[entityHeader];
    });

    res.status = HTTP_STATUS_NOT_MODIFIED;

    res.writeHead(res.status, res.headers);
    res.end();

    server.emit('response', req, res);

    return true;
  } else {
    return false;
  }
}

function parseRanges(req, res, size) {
  var ranges;
  var start;
  var end;
  var i;
  var originalSize = size;

  // support range headers
  if (req.headers.range) {
    // 'bytes=100-200,300-400'  --> ['100-200','300-400']
    if (!RANGE_REQUEST_HEADER_TEST.test(req.headers.range)) {
      return sendError(req, res, null, HTTP_STATUS_BAD_REQUEST, 'Invalid Range Headers: ' + req.headers.range);
    }

    ranges = req.headers.range.match(RANGE_REQUEST_HEADER_PATTERN);
    size = 0;

    if (!ranges) {
      return sendError(server, req, res, null, HTTP_STATUS_BAD_REQUEST, 'Invalid Range Headers: ' + req.headers.range);
    }

    i = ranges.length;

    while (--i >= 0) {
      // 100-200 --> [100, 200]   = bytes 100 to 200
      // -200    --> [null, 200]  = last 100 bytes
      // 100-    --> [100, null]  = bytes 100 to end
      range = ranges[i].split('-');
      start = range[0] ? Number(range[0]) : null;
      end   = range[1] ? Number(range[1]) : null;

      // check if requested range is valid:
      //   - check it is within file range
      //   - check that start is smaller than end, if both are set

      if ((start > originalSize) || (end > originalSize) || ((start && end) && start > end)) {
        res.headers['Content-Range'] = 'bytes=0-' + originalSize;
        return sendError(server, req, res, null, DEFAULT_STATUS_REQUEST_RANGE_NOT_SATISFIABLE);
      }

      // update size
      if (start !== null && end !== null) {
        size += (end - start);
        ranges[i] = { start: start, end: end + 1 };
      } else if (start !== null) {
        size += (originalSize - start);
        ranges[i] = { start: start, end: originalSize + 1 };
      } else if (end !== null) {
        size += end;
        ranges[i] = { start: originalSize - end, end: originalSize };
      }
    }
  }

  return {
    ranges: ranges,
    size: size
  };
}


/**
Send error back to the client. If `status` is not specified, a value
of 500 is used. If `message` is not specified, the default message for
the given status is returned.

@param server {StaticServer} the server instance
@param req {Object}          the request object
@param res {Object}          the response object
@param err {Object}          an Error object, if any
@param status {Number}       the status (default 500)
@param message {String}      the status message (optional)
*/
function sendError(server, req, res, err, status, message) {
  status = status || res.status || HTTP_STATUS_ERR
  message = message || http.STATUS_CODES[status];

  if (status >= 400) {
    // ERR responses should not contain entity headers
    [
      'Content-Encoding',
      'Content-Language',
      'Content-Length',
      'Content-Location',
      'Content-MD5',
      //      'Content-Range', // Error 416 SHOULD contain this header
      'Etag',
      'Expires',
      'Last-Modified'
    ].forEach(function(entityHeader) {
        delete res.headers[entityHeader];
    });

    res.status = status;
    res.headers['Content-Type'] = mime.lookup('text');

    res.writeHead(status, res.headers);
    res.write(message);
    res.end();
  }

  server.emit('response', req, res, err);
}


/**
Send a file back at the client. If the file is not found, an error 404
will be returned. If the file cannot be read, for any reason, an error 500
will be read and the error will be sent to stderr

@param server {StaticServer} the server instance
@param req {Object}          the request object
@param res {Object}          the response object
@param stat {Object}         the actual file stat
@param file {String}         the absolute file path
*/
function sendFile(server, req, res, stat, file) {
  var headersSent = false;
  var contentParts = parseRanges(req, res, stat.size);
  var streamOptions = { flags: 'r' };
  var contentType = mime.lookup(file);
  var rangeIndex = 0;

  if (!contentParts) {
    return;  // ranges failed, abort
  }

  if (!server.noCache) {
    res.headers['Etag']           = JSON.stringify([stat.ino, stat.size, stat.mtime.getTime()].join('-'));
    res.headers['Last-Modified']  = new Date(stat.mtime).toUTCString();
  }

  res.headers['Date']           = new Date().toUTCString();

  if (contentParts.ranges && contentParts.ranges.length > 1) {
    res.headers['Content-Type'] = 'multipart/byteranges; boundary=' + MULTIPART_SEPARATOR;
  } else {
    res.headers['Content-Type']   = contentType;
    res.headers['Content-Length'] = contentParts.size;

    if (contentParts.ranges) {
      res.headers['Content-Range'] = req.headers.range;
    }
  }

  // return only headers if request method is HEAD
  if (req.method === 'HEAD') {
    res.status = HTTP_STATUS_OK;
    res.writeHead(HTTP_STATUS_OK, res.headers);
    res.end();
    server.emit('response', req, res, null, file, stat);
  } else if (!validateClientCache(server, req, res, stat, file)) {

    (function sendNext() {
      var range;

      if (contentParts.ranges) {
        range = contentParts.ranges[rangeIndex++];

        streamOptions.start = range.start;
        streamOptions.end = range.end;
      }

      fs.createReadStream(file, streamOptions)
        .on('close', function () {
          // close response when there are no ranges defined
          // or when the last range has been read
          if (!range || (rangeIndex >= contentParts.ranges.length)) {
            res.end();
            server.emit('response', req, res, null, file, stat);
          } else {
            setImmediate(sendNext);
          }
        }).on('open', function (fd) {
          if (!headersSent) {
            if (!res.status){
              if (range) {
                res.status = HTTP_STATUS_PARTIAL_CONTENT;
              } else {
                res.status = HTTP_STATUS_OK;
              }
            }
            res.writeHead(res.status, res.headers);
            headersSent = true;
          }

          if (range && contentParts.ranges.length > 1) {
            res.write(MULTIPART_SEPARATOR + NEWLINE +
                      'Content-Type: ' + contentType + NEWLINE +
                      'Content-Range: ' + (range.start || '') + '-' + (range.end || '') + NEWLINE + NEWLINE);
          }
        }).on('error', function (err) {
          sendError(server, req, res, err);
        }).on('data', function (chunk) {
          res.write(chunk);
        });
    })();
  }

}