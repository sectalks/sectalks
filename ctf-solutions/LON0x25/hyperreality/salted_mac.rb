#!/usr/bin/env ruby

require "socket"
require "pathname"
require "json"
require "base64"

def admin?(msg)
  msg.include?("admin=yes")
end

# Ruby uses randomized SipHash, good luck breaking that
# Throwing secret key and salt for extra protection against the NSA
def mac(msg, salt)
  (@key + salt + msg).hash
end

def random_salt
  Base64.strict_encode64(Random::DEFAULT.bytes(24))
end

def encrypt(msg)
  salt = random_salt
  {
    msg: msg,
    salt: salt,
    mac: mac(msg, salt),
  }.to_json
end

def decode(cookie)
  decoded_cookie = JSON.parse(cookie)
  msg = decoded_cookie["msg"] or raise
  salt = decoded_cookie["salt"] or raise
  mac = decoded_cookie["mac"] or raise
  raise unless mac(msg, salt) == mac
  if admin?(msg)
    :admin
  else
    :not_admin
  end
rescue
  :bad_cookie
end

def client_session(client)
  client.puts "Welcome to the encryption server"
  client.puts "Commands available:"
  client.puts "* sign - generate a cookie"
  client.puts "* login - login with encrypted JSON cookie"

  cmd = client.gets.chomp
  case cmd
  when "sign"
    client.puts "Enter cookie content to sign:"
    msg = client.gets.chomp
    if admin?(msg)
      client.puts "Admin cookie attempted, but you're not admin"
    else
      cookie = encrypt(msg)
      client.puts "Cookie: #{cookie}"
    end

  when "login"
    client.puts "Enter encrypted cookie:"
    cookie = client.gets.chomp
    client.puts "Received cookie: #{cookie}"

    case decode(cookie)
    when :admin
      flag = Pathname("flag.txt").read.chomp
      client.puts "Login successful"
      client.puts "Flag: #{ flag }"
    when :not_admin
      client.puts "Login as non-admin"
    when :bad_cookie
      client.puts "Bad cookie"
    end
  else
    client.puts "Unrecognized command: #{cmd}"
  end

  client.puts "Goodbye!"
end

@key = Random::DEFAULT.bytes(24)

server = TCPServer.open(9001)
loop do
  Thread.fork(server.accept) do |client|
    begin
      client_session(client)
    ensure
      client.close
    end
  end
end
