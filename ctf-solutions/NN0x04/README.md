# uae (Unhackable App Engine)

```
I've always been annoyed by the cumbersome release and deploy process -- installing correct versions of dependencies, scaling,
load balancing, etc. are just too much for me. My friend recommended this serverless platform that claims to be "unhackable."
I doubt it though...
```

Flag: `sectalks{1_7h0ugh7_0n1y_5ql_15_1nj3ctabl3}`

Like Amazon Lambda. Deploy your website without worrying about VM/containers.

To use this infra, you only need to submit short pieces of code for python functions, see the following example.

The environment is sandboxed.

## Jython

Because of CPython's GIL lock, users can easily DOS the system by having a syscall that takes forever to run.
We use Jython here to have real multithreading.

## How-To

Example deploy:
```
---
urls:
  "/": |-
    uae_rsp = uaeutils.make_response("Hello World")
  "/ping": |-
    uae_rsp = uaeutils.make_response("Pong")
  "/add": |-
    num_a = int(request['args'].get("a"))
    num_b = int(request['args'].get("b"))
    uae_rsp = uaeutils.make_response("Answer is " + str(num_a + num_b))
  "/error": |-
    uae_rsp = uaeutils.errorpage("Oops our server has fallen asleep")
  "/redirect": |-
    uae_rsp = uaeutils.redirect("https://www.adamyi.com/")
  "/json": |-
    uae_rsp = uaeutils.make_response(uaeutils.json_encode({"json": "is_easy"}))
default_handler: |-
  uae_rsp = uaeutils.errorpage("The requested URL %s was not found on this server." % request['path'], code=404)
```

## Source Code Download
Trigger an exception in your python code (e.g. for above, visit `/add?a=1&b=lol`), there will be debug info (stack trace) as well as code download link.

## Vulnerability

Could deploy functions to any domains by injecting caching keys.

**Normal User**
Domain: example
Path: helloworld

Cache Key: example.unhackable.app/helloworld

**Hacker**
Domain: example.unhackable.app/haha
Path: lmao

Cache Key: example.unhackable.app/haha.unhackable.app/lmao

**This would make XSS possible on all UAE apps**

## Flag

Visit https://manage.unhackable.app/edit?app=otp.unhackable.app/adamyi

```
---
urls:
  "/": |-
    uae_rsp = uaeutils.make_response("uh4SGbRbgQCPHnieb2jM1U3BsYZniZmD")
default_handler: |-
  uae_rsp = uaeutils.errorpage("The requested URL %s was not found on this server." % request['path'], code=404)
```

https://otp.unhackable.app/adamyi.unhackable.app/ becomes `uh4SGbRbgQCPHnieb2jM1U3BsYZniZmD`

Use this URL for https://manage.unhackable.app/flag to get flag.

## author
[adamyi](https://github.com/adamyi)
