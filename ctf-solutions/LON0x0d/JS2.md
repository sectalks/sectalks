## LON0x0d JS2

Featuring a webpage with a password field and some nasty JavaScript code. 

Beautifying it doesn't make it look much better:

```javascript
var _0x80a7=['Z2V0RWxlbWVudEJ5SWQ=','cGFzc3dvcmQ=','dmFsdWU=','Y2hhckNvZGVBdA==','bGVuZ3Ro','R3JlYXQgU3VjY2VzcyE=','bG9jYXRpb24=','aHJlZg==','aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1vSGc1U0pZUkhBMA=='];
(function(a, c) {
    var b = function(b) {
        while (--b) {
            a['push'](a['shift']());
        }
    };
    b(++c);
}(_0x80a7, 0xb4));
var _0x780a = function(b, d) {
    b = b - 0x0;
    var a = _0x80a7[b];
    if (_0x780a['initialized'] === undefined) {
        (function() {
            var a;
            try {
                var b = Function('return\x20(function()\x20' + '{}.constructor(\x22return\x20this\x22)(\x20)' + ');');
                a = b();
            } catch (b) {
                a = window;
            }
            var c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
            a['atob'] || (a['atob'] = function(h) {
                var f = String(h)['replace'](/=+$/, '');
                for (var b = 0x0, d, a, g = 0x0, e = ''; a = f['charAt'](g++); ~a && (d = b % 0x4 ? d * 0x40 + a : a, b++ % 0x4) ? e += String['fromCharCode'](0xff & d >> (-0x2 * b & 0x6)) : 0x0) {
                    a = c['indexOf'](a);
                }
                return e;
            });
        }());
        _0x780a['base64DecodeUnicode'] = function(e) {
            var b = atob(e);
            var c = [];
            for (var a = 0x0, d = b['length']; a < d; a++) {
                c += '%' + ('00' + b['charCodeAt'](a)['toString'](0x10))['slice'](-0x2);
            }
            return decodeURIComponent(c);
        };
        _0x780a['data'] = {};
        _0x780a['initialized'] = !![];
    }
    var c = _0x780a['data'][b];
    if (c === undefined) {
        a = _0x780a['base64DecodeUnicode'](a);
        _0x780a['data'][b] = a;
    } else {
        a = c;
    }
    return a;
};

function validate() {
    var a = document[_0x780a('0x0')](_0x780a('0x1'))[_0x780a('0x2')];
    var y = a[_0x780a('0x3')](0x3);
    var z = a[_0x780a('0x3')](0x1);
    var A = a[_0x780a('0x3')](0x9);
    var B = a[_0x780a('0x3')](0x0);
    var C = a[_0x780a('0x3')](0xa);
    var D = a[_0x780a('0x3')](0x2);
    var E = a[_0x780a('0x3')](0x4);
    var F = a[_0x780a('0x3')](0x7);
    var G = a[_0x780a('0x3')](0x5);
    var H = a[_0x780a('0x3')](0x6);
    var m = a[_0x780a('0x3')](0x8);
    var n = C + 0x12;
    var o = F - 0x51;
    var p = E - 0x34;
    var q = A + 0x19;
    var r = G + 0x23;
    var s = z - 0x37;
    var t = y + 0x23;
    var u = D - 0x4c;
    var v = m + 0x43;
    var w = H - 0x7;
    var x = B + 0x7;
    var c = r - 0x95;
    var d = u - 0x22;
    var e = q - 0x83;
    var f = w - 0x60;
    var b = t - 0x91;
    var h = x - 0x69;
    var i = s - 0x3a;
    var j = n - 0x84;
    var k = p - 0x36;
    var l = v - 0xb0;
    var g = o - 0xf;
    if (a[_0x780a('0x4')] == 0xb && g * h * j * f * c * l * e * i * d * b * k == 0x1 && j + e + b + g + i + l + c + h + k + f + d == 0xb) {
        alert(_0x780a('0x5'));
    } else {
        document[_0x780a('0x6')][_0x780a('0x7')] = _0x780a('0x8');
    }
}
```

There are a lot of `_0x780a(HEX)` function calls, which we can transform back into legible strings in the browser console to give a clearer idea of what is going on. For instance:

```javascript
> _0x780a('0x8')
"https://www.youtube.com/watch?v=oHg5SJYRHA0"
```

Which also happened to be the most important-looking variable in the `else` branch of the validate function. And which also turns out to be a rickroll (of course). Meaning that the true branch is what we need to go down for the solution:

```javascript
if (a.length == 11 && g * h * j * f * c * l * e * i * d * b * k == 1 && j + e + b + g + i + l + c + h + k + f + d == 11)
```

So 11 variables need to multiply together to give 1, and add together to 11. This occurs when they all equal 1. How are they calculated then? Picking `g`:

```javascript
var F = a.charCodeAt(7);
var o = F - 0x51;
var g = o - 0xf;
```

Take the UTF-16 value of the 7th index of the password, subtract 0x51 and 0xf from it. Stepping back through this process in the indispensable Python console:

```python
> chr(1 + 0xf + 0x51)
'a'
```

We can see that 'a' is the 8th character. Rinse and repeat for the other characters and we are done. 

We could also use a constraint solver like [z3](https://github.com/Z3Prover/z3), but given that the solution was only 11 characters long and probably guessable after figuring out 4 or 5 of them, it wasn't worth setting up.

It was interesting to note that the `_0x780a` function was just an obfuscated base64-decoder, but that we didn't need to know that to solve this one.
