class Integer
  def to_s_binary
    i = self
    out = []
    while i > 0
      c = i & 0xff
      i >>= 8
      out << c
    end
    out.pack("C*").reverse
  end
end

class String
  def to_i_binary
    unpack("C*").reduce(0) do |a,b|
      a*256 + b
    end
  end
end


def extended_gcd(a, b)
  last_remainder, remainder = a.abs, b.abs
  x, last_x, y, last_y = 0, 1, 1, 0
  while remainder != 0
    last_remainder, (quotient, remainder) = remainder, last_remainder.divmod(remainder)
    x, last_x = last_x - quotient*x, x
    y, last_y = last_y - quotient*y, y
  end
 
  return last_remainder, last_x * (a < 0 ? -1 : 1)
end
 
def invmod(e, et)
  g, x = extended_gcd(e, et)
  if g != 1
    raise 'The maths are broken!'
  end
  x % et
end


n=26508718324564454851483195255536724615774858683210632188681647178370472690716622966269956634868472082937057902195079877331595276679883088195760584638497574904852097341988303883826026676908963196983242128359326617225036051113468880894300374873382012566577042354337256910729401119610719829590277067261583243640121852685704992963253574510435374023393111175858864331623764790732153680979485293137410714910908390220862030589339538766994038504908988819194690629301328989706455744115713587246404587643184371530547757235172724483615726523768387717467893982484964884655048039254854968099068853676196709587833067505446139649641
naughty = "admin=yes"
const = "a"
multiplied = (naughty.to_i_binary * const.to_i_binary).to_s_binary

require 'socket'

def get_signature(input)
  s = TCPSocket.open('mtg.wtf', 9002)

  puts s.gets
  puts s.gets
  puts s.gets
  puts s.gets
  puts s.gets
  puts s.gets

  s.puts "sign"
  puts s.gets

  s.puts input

  signature = s.gets.split[1]
  s.puts

  s.close

  signature
end

sig_m = get_signature(multiplied).to_i
sig_k = get_signature(const).to_i

out = (sig_m * invmod(sig_k, n)) % n

puts out

s = TCPSocket.open('mtg.wtf', 9002)
puts s.gets
puts s.gets
puts s.gets
puts s.gets
puts s.gets
puts s.gets

s.puts "admin"
puts s.gets

s.puts naughty
puts s.gets

s.puts out
puts s.gets
s.puts
puts s.gets
