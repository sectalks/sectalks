This is how I created the challenge.

The differents steps are:

- Find the XOR key and get the image back;
- Find the encoding mechanism in the image and extract the binary data;
- Convert the binary to ASCII
- Execute the found code

The code used to create the final HTML document can be found in `hide.py`, and the code used to decode the image part, in `show.py`.

---

# JSFuck

The boring end-of-the-ctf flags is "Well done.".

Encode this string with [jsfuck](http://www.jsfuck.com/), you can see the result in the file `jsfuck.js`.

# Binary conversion

This step is just converting the `jsfuck` text generated above to a clear binary string so that we can use it in the image encoding.

I relied entirely on the python `binascii` library to do that.

# Image encoding

The way I did the encoding, was to rely on the fact that seeing very little changes in the shades of gray is really hard. So I converted an image to a pure gray image, and switched some of RGB values by 1, depending on the encoding I wanted to have.

For a `1` I would encode `XYY` and for a `0` `YXY` for the RGB values. So the file is technically not gray, but really close to.

# Base64

After this, I converted the image under a `PNG` format and converted it to its `base64` representation. I'm creating the final image string by prepending the string `data:image/png;base64,`, which makes the whole string a valid image source.

# XOR

Then I would use the XOR key to XOR the entire string generated previoulsy. Only the first 10 chars are used, because it would be too hard to guess a key longer than the fixed `data:image` prefix.

# HTML

Finally, include the array, verbattim in the HTML document, and save it as `challenge.html`.
