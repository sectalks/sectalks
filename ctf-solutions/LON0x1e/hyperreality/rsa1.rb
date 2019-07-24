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


naughty = "admin=yes"
n=22904344199460192534586256373909482003878694407491484273321362123549183574143605519746934335687308804051748841673737020751985684204907836720752948660487506174714469434487277462201531940658474190055095402973141184584712518052646627127737839932336996490740101550874270019969176586649675460906037094177843980185900990156972176916265720359724562452428597201830286922077014802869413793239688056101596349855775576954954237820466907406204874678915841896467235831344140922638204287455653182658002485779425401196139259205148415583311720722312374907772972139811058319604504857555740613492516269877162231044895526904973794209861

a = (naughty.to_i_binary + n).to_s_binary

# File.write('bla', a)
# system('bash -c "cat <(echo sign; sleep 1; cat bla; echo; exit) - | nc mtg.wtf 9001"')

require 'socket'

s = TCPSocket.open('mtg.wtf', 9001)

puts s.gets
puts s.gets
puts s.gets
puts s.gets
puts s.gets
puts s.gets

s.puts "sign"
puts s.gets

s.puts a

signature = s.gets
s.puts
puts s.gets

puts signature.split[1]

s.close

s = TCPSocket.open('mtg.wtf', 9001)
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

s.puts signature.split[1]
puts s.gets
s.puts
puts s.gets
