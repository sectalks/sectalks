#!/usr/bin/env ruby

require "socket"
require "pathname"
require "json"
require "base64"
require "openssl"

def admin?(msg)
  msg.include?("admin=yes")
end

# 128-bit unpack
def unpack(str)
  str.bytes.each_slice(16).map do |slice|
    slice.map.with_index{|c, i| c * (256 ** i)}.sum
  end
end

# It's exactly one block so ECB mode
def encrypt_nonce(nonce)
  block = "%016d" % nonce
  cipher = OpenSSL::Cipher.new("AES-128-ECB")
  cipher.encrypt
  cipher.key = @key_aes
  cipher.padding = 0
  encrypted = cipher.update(block) + cipher.final
  unpack(encrypted)[0]
end

# TODO: Double check that this is what Poly1305 does
# Not sure I follow all the details
def poly_mac(msg, nonce)
  prime = 2**130 - 5
  z = 0
  ri = @key_r
  # Evaluate polynomial
  unpack(msg).each_with_index do |mi, i|
    z = (z + mi * ri) % prime
    ri = (ri * @key_r) % prime
  end
  # Apply nonce
  aes_n = encrypt_nonce(nonce)
  (z + aes_n) % prime
end

# It doesn't need to be random
# It causes birthday paradox issues to pick random one
# Sequential is totally safe
def new_nonce
  Time.now.to_i
end

def encrypt(msg)
  nonce = new_nonce
  {
    msg: msg,
    nonce: nonce,
    mac: poly_mac(msg, nonce)
  }.to_json
end

def decode(cookie)
  decoded_cookie = JSON.parse(cookie)
  msg = decoded_cookie["msg"] or raise
  nonce = decoded_cookie["nonce"] or raise
  mac = decoded_cookie["mac"] or raise
  raise unless poly_mac(msg, nonce) == mac
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

# Poly1305 has two part key
@key_aes = Random::DEFAULT.bytes(16)
@key_r   = rand(2**128)

server = TCPServer.open(9002)
loop do
  Thread.fork(server.accept) do |client|
    begin
      client_session(client)
    ensure
      client.close
    end
  end
end
