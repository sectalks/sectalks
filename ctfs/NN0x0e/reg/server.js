'use strict';

const fs = require("fs");
const express = require("express");
const zlib = require("zlib");

const PORT = 8080;
const HOST = "0.0.0.0";

const allowCharRegex = /[^a-zA-Z0-9 ]/;
const hasNonPrintable = (s) => allowCharRegex.test(s);
const escapeHTML = s => s.replace(/[&<>'"]/g,
  tag => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#39;",
      "\"": "&quot;"
    }[tag]));

const app = express();

app.use(
  express.urlencoded({
    extended: true
  })
);

app.use(express.json())

function doCompression(query, res) {
  if (query === null || hasNonPrintable(query) || Array.isArray(query)) {
    res.status(500);
    res.send({
      "error": "Failed to run query."
    });
  } else {
    // Compress in-process (gzip + base64) instead of piping the value through a
    // shell. The request value can no longer reach a command interpreter.
    try {
      const data = zlib.gzipSync(Buffer.from(query, "utf8")).toString("base64");
      res.status(200);
      res.send({
        "data": data
      });
    } catch (e) {
      res.status(500);
      res.send({
        "error": `${e.message}`
      });
    }
  }
}

app.get("/compress", function(req, res) {
  doCompression(req.query.query, res);
});

app.post("/compress", function(req, res) {
  doCompression(req.body.query, res);
});

app.get("/code", function(req, res) {
  try {
    let data = fs.readFileSync("server.js", "utf8");
    res.send(`<html><body><pre>${escapeHTML(data.toString())}</pre></body></html>`);

  } catch (e) {
    res.send("Something went wrong, contact the CTF developer.");
  }
});

app.get("/", (req, res) => {
  let data = fs.readFileSync("index.html", "utf8");
  res.send(data.toString());
});

app.listen(PORT, HOST);
console.log(`Running bad-regex on http://${HOST}:${PORT}`);
