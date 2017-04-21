## LON0x08 Solution

We are presented with a HTML document containing a single very long line of  Javascript that executes on page load:

```html
<body onload="a=String.fromCharCode;String.prototype.b=String.prototype.charCodeAt;Number.prototype.c=Number.prototype.toString;key=prompt('Enter the key');document.body.innerHTML='<img src='+[23, 4, 23, 21, 91, 5, 6, 18
...
46, 86, 55, 56, 37, 34, 78].map((e,i)=>a(e^key[i%10].b(0).c(10))).join('')+' />';"></body>
```

It's an array of numbers so large that it crashes text editors, with some cryptic javascript functions at the beginning and end. When opened in the browser, the code simply presents a password prompt. Let's try and work out what it's doing.

At first there is a reassignment of various functions inherent to the Javacript String and Number types to single letter variables, most likely as a means of obfuscation. Substituting these into the function at the end, we get:

```javascript
[big array].map((e,i)=>String.fromCharCode(e^key[i%10].charCodeAt(0).toString(10))).join('')
```

The map parameters are e, the current element of the array, and i, the index of that element. So the code is XORing each element of the array with the index mod 10th value of the key (after that value has been transformed into a numerical ASCII code). Already we can assume that the key is 10 characters long.

Since XOR is a reversible operation, i.e. if we do A XOR B = C then we can do C XOR B to get back A again, if we can guess the first few characters of the result string we should be able to obtain the key.

As the cipher string is preceded by `<img src=`, a very logical guess as to what will follow is the beginning of a URL, `http`. I tried a lot of variations on this without it yielding any results. Taking a second look at the length of the array and realising that there was probably far too much of it to be a URL, I wondered, maybe it was image data itself...?

This jogged my memory about a widely-reported [Gmail phishing](https://www.wordfence.com/blog/2017/01/gmail-phishing-data-uri/) campaign that was doing the rounds a few months ago. The attackers used a special `data:text/html` type of URL with an inline webpage. Wikipedia has [an example](https://en.wikipedia.org/wiki/Data_URI_scheme#Examples_of_Usage) of the Data URI scheme being used to include image data.

So perhaps the ciphertext would start `data:image`, which has 10 characters.

```python
Python 2.7
>>> guess = "data:image"
>>> arr = [23, 4, 23, 21, 91, 5, 6, 18, 91, 86]
>>> ''.join([chr(arr[i] ^ ord(guess[i])) for i in range(10)])
'sectalks<3'
```

Bingo! After typing this key into the password prompt we are presented with an image:

![](grey.png)

I didn't recognise it, but a quick reverse image search said "Fifty Shades of Grey", apparently a clue to the next step. A close visual inspection didn't reveal anything so I investigated the RGB colour codes of the first row of the image using Python's excellent Python Imaging Library:

```python
>>> from PIL import Image
>>> image = Image.open("grey.png")
>>> w, h = image.size
>>> w
469
>>> h
699
>>> im = image.load()
>>> for i in range(w):
...     print(im[0,i])
(246, 245, 245, 255)
(249, 248, 248, 255)
(246, 247, 246, 255)
(247, 248, 247, 255)
(247, 248, 247, 255)
(246, 247, 246, 255)
(250, 249, 249, 255)
(246, 245, 245, 255)
...
```
Immediately, something stood out: most of the pixels are grey with uniform R,G,B values but some colour values are incremented by one.

After trying some things I came up with code that outputted promising looking binary: traverse all pixel rows of the image; if the R value is incremented, it's a 1; if the G is incremented, it's a 0. If it's a grey pixel then ignore. I then chunked the output binary string into groups of bytes:

```python
from PIL import Image
image = Image.open("grey.png")
w, h = image.size
im = image.load()

arr = []

for i in range(h):
      for j in range(w):
          rgb = im[j,i]

          if (rgb[0] != rgb[1]):
              if (rgb[1] != rgb[2]):
                  arr.append('0')
              else:
                  arr.append('1')

def chunks(l, n):
        return (l[i:i+n] for i in xrange(0, len(l), n))

print([''.join(i) for i in chunks(arr, 8)])

['10110110', '10111010', '10110110', '01010000', '01000010', '10110110', '10111010', '01010110' ...
```

And yet after converting these numbers to ASCII codes and then to a string, the result was garbage. Nevertheless, the distribution of the numbers looked very encouraging, with many repeating patterns. After many more manipulations and some consultations with the challenge setter, he gave a hint about the binary encoding. 

The problem was to do with printing 8 bit chunks whereas ASCII codes are 7 bits. However, printing in 7 bit chunks didn't produce a comprehensible result either. It turned out that during the creation of the image the first 0 bit was lost, so simply adding that to the beginning of the array (or alternatively dividing all of the numbers by two, which is equivalent to a right bit shift), all the numbers would be moved along, making them printable ASCII.

Here is the final code:

```python
from PIL import Image
image = Image.open("grey.png")
w, h = image.size
im = image.load()

arr = ['0']

for i in range(h):
      for j in range(w):
          rgb = im[j,i]

          if (rgb[0] != rgb[1]):
              if (rgb[1] != rgb[2]):
                  arr.append('0')
              else:
                  arr.append('1')

def chunks(l, n):
        return (l[i:i+n] for i in xrange(0, len(l), n))

result = [chr(int(''.join(i), 2)) for i in chunks(arr, 8)]

print(''.join(result))
```

The output string was a long series of square brackets, pluses, and other unsightly characters. At this point I got excited because it looked like Brainfuck, but pasting it into an interpreter just caused my browser to freeze. 

In the meantime I looked at the Brainfuck [wiki page](https://en.wikipedia.org/wiki/Brainfuck) and realised the language doesn't include exclamation marks, which the string included plenty of. Perhaps it was JSFuck instead? After it into the browser console and hitting enter, I was presented with a friendly "well done" message.

Thanks [nobe4](https://github.com/nobe4) for a great challenge!

