#SYD0x10 CTF Writeups#
##### By SteffnJ #####

## Introduction ##
You are given a website: http://188.166.235.114/ and a hint that there are two main flags.

## Flag 1 ##
After playing around with various aspects such as checking source-code, cookies, parameters, etc, we realized that the search box seems vulnerable. This is verified by typing `'` as a search string. This gives the error: `Error in query: SELECT * FROM posts WHERE public = 1 AND content LIKE '%'%'`. Now that we have found something that seems vulnerable to a SQL injection, we need to find out exactly how it works and how we can exploit it. After playing around a bit more with a string such as `'hello world`, we can clearly see this: `Error in query: SELECT * FROM posts WHERE public = 1 AND content LIKE '%'hello%'`. Interesting! It seems that whitespaces is used as a delimiter and ignores everything after the first whitespace. 

Since `' or 1=1;--` does not seem to work (the latter semicolon and double hyphens are to comment out the rest of the field and therefore escaping the `%` wildcard used), we will have to find other ways. Perhaps we can use multiline comments? After trying with `'/**/or/**/1=1;--` we archieve success! The flag shows up as a blog entry on the result page (along with all other blog entries): flag{bb020edd4cb6f01132259bbb761ca2d5}


## Flag 2 ##
