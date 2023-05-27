require('core-js/stable');
var express = require('express');
var { graphqlHTTP } = require('express-graphql');
var { buildSchema } = require('graphql');

var schema = buildSchema(`
  type Query {
    "This method is not correct"
    flag1: String 
    "This method is not correct"
    flag2: String 
    "This method is not correct"
    flag3: String 
    "This method is not correct"
    flag4: String 
    "This method is not correct"
    flag5: String 
    "This method is not correct"
    flag6: String 
    "This method is not correct"
    flag7: String 
    "This method is not correct"
    flag8: String 
    "This method is not correct"
    flag9: String 
    "This method is not correct"
    flag10: String 
    "This method is not correct"
    flag11: String 
    "This method is not correct"
    flag12: String 
    "This method is not correct"
    flag13: String 
    "This method is not correct"
    flag14: String 
    "This method is not correct"
    flag15: String 
    "This method is not correct"
    flag16: String 
    "This method is not correct"
    flag17: String 
    "This method is not correct"
    flag18: String 
    "This method is not correct"
    flag19: String 
    "This method is not correct"
    flag20: String 
    "This method is not correct"
    flag21: String 
    "This method is not correct"
    flag22: String 
    "This method is not correct"
    flag23: String 
    "This method is not correct"
    flag24: String 
    "This method is not correct"
    flag25: String 
    "This method is not correct"
    flag26: String 
    "This method is not correct"
    flag27: String 
    "This method is not correct"
    flag28: String 
    "This method is not correct"
    flag29: String 
    "This method is not correct"
    flag30: String 
    "This method is not correct"
    flag31: String 
    "This method is not correct"
    flag32: String 
    "This method is not correct"
    flag33: String 
    "This method is not correct"
    flag34: String 
    "This method is not correct"
    flag35: String 
    "This method is not correct"
    flag36: String 
    "This method is not correct"
    flag37: String 
    "This method is not correct"
    flag38: String 
    "This method is not correct"
    flag39: String 
    "This method is not correct"
    flag40: String 
    "This method is not correct"
    flag41: String 
    "This method is not correct"
    flag42: String 
    "This method is not correct"
    flag43: String 
    "This method is not correct"
    flag44: String 
    "This method is not correct"
    flag45: String 
    "This method is not correct"
    flag46: String 
    "This method is not correct"
    flag47: String 
    "This method is not correct"
    flag48: String 
    "This method is not correct"
    flag49: String 
    "This method is not correct"
    flag50: String 
    "This method is not correct"
    flag51: String 
    "This method is not correct"
    flag52: String 
    "This method is not correct"
    flag53: String 
    "This method is not correct"
    flag54: String 
    "This method is not correct"
    flag55: String 
    "This method is not correct"
    flag56: String 
    "This method is not correct"
    flag57: String 
    "This method is not correct"
    flag58: String 
    "This method is not correct"
    flag59: String 
    "This method is not correct"
    flag60: String 
    "This method is not correct"
    flag61: String 
    "This method is not correct"
    flag62: String 
    "This method is not correct"
    flag63: String 
    "This method is not correct"
    flag64: String 
    "This method is not correct"
    flag65: String 
    "This method is not correct"
    flag66: String 
    "This method is not correct"
    flag67: String 
    "This method is not correct"
    flag68: String 
    "This method is not correct"
    flag69: String 
    "This method is not correct"
    flag70: String 
    "This method is not correct"
    flag71: String 
    "This method is not correct"
    flag72: String 
    "This method is not correct"
    flag73: String 
    "This method is not correct"
    flag74: String 
    "This method is not correct"
    flag75: String 
    "This method is not correct"
    flag76: String 
    "This method is not correct"
    flag77: String 
    "This method is not correct"
    flag78: String 
    "This method is not correct"
    flag79: String 
    "This method is not correct"
    flag80: String 
    "This method is not correct"
    flag81: String 
    "This method is not correct"
    flag82: String 
    "This method is not correct"
    flag83: String 
    "This method is not correct"
    flag84: String 
    "This method is not correct"
    flag85: String
    "This method is not not correct"
    flag86: String 
    "This method is not correct"
    flag87: String 
    "This method is not correct"
    flag88: String 
    "This method is not correct"
    flag89: String 
    "This method is not correct"
    flag90: String 
    "This method is not correct"
    flag91: String 
    "This method is not correct"
    flag92: String 
    "This method is not correct"
    flag93: String 
    "This method is not correct"
    flag94: String 
    "This method is not correct"
    flag95: String 
    "This method is not correct"
    flag96: String 
    "This method is not correct"
    flag97: String 
    "This method is not correct"
    flag98: String 
    "This method is not correct"
    flag99: String 
    "This method is not correct"
    flag100: String 
  }
`);

// The root provides a resolver function for each API endpoint
var root = {
  flag86: () => {
    return 'sectalks{br11ng1ng_n1ck3l_back}';
  },
};

var app = express();

app.get('/', function(request, response){
    response.sendFile('/app/index.html');
});

app.get('/index.html', function(request, response){
    response.sendFile('/app/index.html');
});

// app.get('/graph_meme.png', function(request, response){
//     response.sendFile('/app/graph_meme.png');
// });

app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: false,
}));
app.listen(4000, '0.0.0.0');
console.log('This web server is running a GraphQL API server');
