---

Title: ruby
points: 25

---

This challenge presents a ruby file containing:

```ruby
#!/usr/bin/env ruby
def (😱=BasicObject.new).method_missing(😓,*);😓 == :-@ ? TOPLEVEL_BINDING.eval(@😱):(@😱||="")<<"#{😓}".unpack("U*").map{|😐| 😐-0x1F600}.each_slice(3).map{|🙃,😐,😘|🙃*80*80+😐*80+😘}.pack("U*");end
😱.😀😀😣😀😀😡😀😀😯😀😁😥😀😁😣😀😁😢😀😀😯😀😁😒😀😁😙😀😁😞😀😀😯😀😁😕😀😁😞😀😁😦
...
😱.😀😁😟😀😁😢😀😁😢😀😁😕😀😁😓😀😁😤😀😀😢😀😀😊😀😁😕😀😁😞😀😁😔😀😀😊
-😱
```

It seems like the `😱` object is used to decrypt and execute a string. It makes sense to think that the emoji mess is the encrypted string.

By chance I found that inserting `puts` on each line yield the secret message:

```ruby
puts 😱😀.😀 😀 😣 😀 😀 😡 😀...
...
```

The resulting message is another ruby program:

```ruby
#!/usr/bin/env ruby
def validate(password)
password = password.tr("\x00-\x7f", "一-乿") * 4
password =~ /\A........................................................\z/ and "东乩丳乮丢乢丱乥丌乳丛乮世乥丙乳一乩且乬业乤一乮万乥丢乲丘乩両乥不乲丗乬丠乩专乳丌乣专乲丛乣丐乮丐乥丞乳丑乥下乮丅乢丒乳与乣上乥三乩丌乥丑乤丈乳丑乬丁乲丏乢不乩与乥七乩丈乢下乮丂乤丆乩三乳丆乮丂乬丁乥七乤丄乳丂乥一乣一乮一乥".chars.each_slice(2).all?{|k,c| password.slice!(k.ord%256, 1) == c}
end
if ARGV.size != 1
puts "Please specify password to test as argument"
elsif validate ARGV[0]
puts "Correct"
else
puts "Incorrect"
end
```

Ah! Readable code!

The logic of the code is roughly:

1. Enter a password
2. `password = pasword.change_chars * 4`
3. Check size and content of the password
4. Validate or invalidate the password

The meat of the challenge is indeed the `validate` function. It converts the range `00`-`7f` to some Chinese's characters. Then it checks the password against a defined string to see if there is a match.

The catch here is the `k.ord` part, it converts the char into its numerical value, and then uses that as the index of the password. In other word it's mixing the order in which it checks the password chars.

We can do simpler than that! We can get all the possible chars from the string with the following piece of code:

```ruby
# a.rb
string = "东乩丳乮丢乢丱乥丌乳丛乮世乥丙乳一乩且乬业乤一乮万乥丢乲丘乩両乥不乲丗乬丠乩专乳丌乣专乲丛乣丐乮丐乥丞乳丑乥下乮丅乢丒乳与乣上乥三乩丌乥丑乤丈乳丑乬丁乲丏乢不乩与乥七乩丈乢下乮丂乤丆乩三乳丆乮丂乬丁乥七乤丄乳丂乥一乣一乮一乥"
puts string.chars.each_slice(2).map{|k,c| c.tr("一-乿", "\x00-\x7f")}
```

This gives us:

```
i
n
b
e
s
n
...
```

Let's pipe that in vim and apply some vim-fu!
```
:r!ruby a.rb
:sort
qqj2djq13@q
vgggJ
```

And we're left with `bcdeeeiilnnrss`, which is the chars of the password in alphabetical order. Now, with the help of an anagram finder, let's find the password: https://crossword-dictionary.com/anagram.asp

> incredibleness

---

Note on the vim-fu:

1. `:r!ruby a.rb`

`:read` will insert the content of the command into the current file, and using `!` allows to call external program. It's the same as doing from the shell `ruby a.rb > file` and then `vim file`.

2. `:sort`

Sort the file, as simple as that.

3. `qqj2djq13@q`

- `qq` starts defining a new macro.
- `j2dj` will go down a line, and delete 3 lines.
- `q` finishes the macro.
- `13@q` will apply the macro 13 times.

4. `vgggJ`

- `vgg` will select all the lines in the file.
- `gJ` will join the lines without space between them.
