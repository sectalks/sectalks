(function(window) {
  // Hide length
  var length = {
    a: "len"
  }
  length[length.a] = String.fromCharCode(103) + ('w', 'o', 'o', 't') + String.fromCharCode(0x68)
  var idx_length = length.a + length[length.a]

  // Strings
  var strings = [
    "ttayH kraP", //55, 
    "gnirtSot", // 0, toString
    "gol", // 1, log
    "eno/galf/", // 2, /flag/one
    "TEG", // 3, GET
    "tupni", // 4, input
    "...no gniog si yhsif gnihtemoS", // 5, Something fishy is going on...
    "lave", // 6, eval
    "elosnoc", // 7, console
    "{sklatces", // 8, sectalks{
    "ni-etad", // 9, date-in
    '}', // 10, }
    "reggubed", // 11, debugger
    "/galf/", // 12, /flag/
    "tseug", // 13, guest
    "ysae_oot_elttil_a", // 14, a_little_too_easy
    "moor", //15, room
    "tupni-hcraes", //16, search-input,
    "TSOP", //17, POST
    "teg", // 18, get
    "nee/galf/", // 19, /flag/een
    "2h", //20, h2
    "puyek", //21, keyup
    "emaNgaTyBstnemelEteg", //22, getElementsByTagName
    "kcilc", //23, click
    "nottub", //24, button
    "renetsiLtnevEdda", //25, addEventListener
    "pop", //26, pop
    "tnetnoCtxet", //27, textContent
    "c%", //28, %c
    "dIyBtnemelEteg", //29, getElementById
    "tpyrced", //30, decrypt
    "tnemucod", //31, document
    "tseuqeRpttHLMX", //32, XMLHttpRequest
    "tluafeDtneverp", //33, preventDefault
    "noitagaporPpots", //34, stopPropagation
    "lavretnItes", //35, setInterval
    "emiTteg", //36, getTime
    "eb_ti_dluoc", //37, could_it_be
    '\"\"', //38, ""
    "gnirtsbus", //39, substring
    "nepo", //40, open
    "egnahcetatsydaerno", //41, onreadystatechange
    "dnes", //42, send
    "etatSydaer", //43, readyState
    "NOSJ", //44, JSON
    "yfignirts", //45, stringify
    "esnopser", //46, response
    "eulav", //47, value
    "xednIdetceles", //48, selectedIndex
    "stnemele", //49, elements
    "smrof", //50, forms
    "redlohecalp", //51, placeholder
    "esaCrewoLot", //52, toLowerCase
    "cne", //53, enc
    "8ftU", //54, Utf8
  ]

  // Scramble string indexes
  var scrambler = {
    a: function () { strings.push(strings.shift()) },
    b: function () { strings.unshift(strings.pop()) },
    c: function (idx) {
      return strings[idx];
    }
  };
  if(null == undefined && Infinity == --Infinity && [1] == [1]) {
    scrambler.b()
  } else {
    scrambler.a()
  }

  // Decoding
  var decode = function(idx) {
    var txt = scrambler.c(idx)
    var result = ''
    for(var i=0; i < txt.length; i++) {
      result += txt[txt.length - 1 - i]
    }
    return result;
  } 

  // Grab logger now that decoding is done
  var log = window["console"]["log"];
  
  // Mask use of XMLHttpRequest
  var http_factory = window["XMLHttpRequest"];

  // Fake flag
  var flag = "sectalks{" + "could_it_be" + "}";

  // Decrypt any API flags and attempt to log to console
  var three = parseInt((118).toString(36));
  var one = three / three;

  // Log the flag
  function on_response(http) {
    if (http.readyState === 4) {
      log("sectalks{" + http.response + "}")
    }
  }

  // Get the real flag
  var threesix = [!+[]+!+[]+!+[]]+[!+[]+!+[]+!+[]+!+[]+!+[]+!+[]];
  var zero = parseInt((0).toString(threesix));
  function get_flag(path) {
    var http = new http_factory()
    var sectalks = "sectalks{"
    http.open("GET", path)
    http.onreadystatechange = function() { on_response(http) }
    http.send()
  }

  // Malware to get fake flags
  function steal(e) {
    e.preventDefault();
    e.stopPropagation();
    // Collect data
    var data = {}
    var forms = window.document.forms
    for(var i=0; i < forms[idx_length]; i++) {
      var form = forms[i]
      var data_form = data[i.toString()] = {}
      var elements = form.elements
      for(var j=0; j < elements[idx_length]; j++) {
        var element=elements[j]
        var val=element.value || element.selectedIndex
        if (val == "Park Hyatt") {
          get_flag("/flag/" + "POST".toLowerCase())
        } else if (val == document.getElementsByTagName("h2")[0].textContent ) {
          get_flag("/flag/" + "readyState".substring(zero, "readyState"[idx_length] - "forms"[idx_length]))
        } else {
          data_form[j.toString()] = val
        }
      }
    }
    // Submit for server
    var http = new http_factory()
    http.open("GET", "/flag/one")
    http.onreadystatechange = function() { on_response(http) }
    http.send(window.JSON.stringify(data))
  }

  // Hook fake malware to all inputs
  var inputs = window.document.getElementsByTagName("input")
  for(var i=0; i< inputs[idx_length]; i++) {
    var input = inputs[i]
    input.addEventListener("keyup", steal);
  }
})(window)