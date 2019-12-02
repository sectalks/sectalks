#!/usr/bin/env ruby

require "socket"
require "pathname"
require "json"
require "zlib"

def admin?(msg)
  msg.include?("admin=yes")
end

def crc32_mac(msg)
  Zlib.crc32(@key + msg)
end

def encrypt(msg)
  {
    msg: msg,
    mac: crc32_mac(msg),
  }.to_json
end

def decode(cookie)
  decoded_cookie = JSON.parse(cookie)
  msg = decoded_cookie["msg"] or raise
  mac = decoded_cookie["mac"] or raise
  raise unless crc32_mac(msg) == mac
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

server = TCPServer.open(9000)
loop do
  Thread.fork(server.accept) do |client|
    begin
      client_session(client)
    ensure
      client.close
    end
  end
end
