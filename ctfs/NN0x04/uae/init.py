import redis
r = redis.Redis(host="redis", port=6379, db=0)
r.set("user/admin", "noONEcanGUESSmeLoLadamyi")
r.set("owner/otp", "admin")
r.set("owner/manage", "admin")
r.set("owner/admin", "admin")
r.set("owner/flag", "admin")
r.set("owner/www", "admin")
r.set(
    "code/otp", """---
urls:
  "/": |-
    uae_rsp = uaeutils.make_response("<h1>Employee Secret Key Database</h1>This is our brand new authentication service. If you are an employee, you should be able to add your OTP (one-time password) to this site. Internal services can then access this site with the URL you provided to check if your OTP is here. If your OTP is hosted on this site, it means you are authenticated as an unhackable.app employee :)")
default_handler: |-
  uae_rsp = uaeutils.make_response("this OTP url doesn't exist :(")
""")
