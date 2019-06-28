### Buzzwagon

I wrote this simple program:

```ruby
    #!/usr/bin/env ruby

    require "socket"
    require "pry"

    s = TCPSocket.new "c.ctf.turtleturtleup.com", 1338

    while true
      line = s.readline
      puts line

      case line
      when /I'm thinking of a number between (\d+) and (\d+). What is it?/
        min = $1.to_i
        max = $2.to_i

        mid = (min + max) / 2
        s.puts mid
      when /Higher/
        min = mid + 1
        mid = (min + max) / 2
        s.puts mid
      when /Lower/
        max = mid - 1
        mid = (min + max) / 2
        s.puts mid
      when /Correct/
      when /Too many guesses. Better luck next time/
        break
      else
        binding.pry
      end
    end
```

### All in the hips

It's probably a Mersenne Twister, but it's easier to just connect twice and copy answers from one to the other.

```sh
    ruby -e '200.times{ puts "1 2 3 4 5 6 7 8" }' | nc c.ctf.turtleturtleup.com 1340 | pcregrep '\[' | perl -ple 's/.*\[//; s/\]//' > numbers.txt
```

Those numbers could then get copypasta'd into the prompt. For some reason (possibly related to timing and buffer sizes) direct `nc` didn't work, but manual copypasta did.

### Stepping stone

It could be solved manually.

### Time is short

There was some bug in the program, and somehow smashing random garbage solved it. No idea how.

### Wallhack

After viewing the problem in Ghidra, I ran it in gdb to modify the maze.

Session went something like this:

```
    (gdb) break tile_is_free
    (gdb) run
    d
    (gdb) print (char[30])maze
    $1 = '#' <repeats 14 times>, "@    #    B#####"
    (gdb) set ((char[30])maze)[19] = ' '
    (gdb) print (char[30])maze
    $2 = '#' <repeats 14 times>, "@         B#####"
    (gdb) delete
    (gdb) c
```

That removed the wall between me and the goal.

### No-show

I did it after Wallhack, so I had some idea how maze would be encoded.

I grepped the source and there was ASCII art. With a `pry` session:

```ruby
    (main)> d=open("noshow","rb").read; p [d.index(/###/), d.rindex(/###/)]
    => 24932
    (main)> puts d[24704..24934].scan(/.{11}/)
    ###########
    #@      # #
    ### # ### #
    #   #     #
    # ### ### #
    # #     # #
    ### # ### #
    #   #   # #
    # # # ### #
    # # # #   #
    ### ##### #
    #     #   #
    ### ### # #
    #   #   # #
    # # ### # #
    # # #   # #
    # # ### # #
    # #   # # #
    # # # # ###
    # # # #  B#
    ###########
```

### Ship it #1

I tried to actually run them in docker, but it was a waste of time, and just unpacking docker image ended up much more useful.

Using `unall` from https://github.com/taw/unix-utilities because who can remember all the flags for all the unpackers.
It also makes sure to create uniquely named folder for each archive, get rid of archive after it's unpacked etc.

```
    docker save bizzaroturtle/ctf:shipit-01 -o s1.tar
    unall s1.tar
    unall */layer.tar
    cat */*.txt
```

### Ship it #2

After unpacking the docker image:

```
    ./dog ../0e5c393aa58d66b887ed3921ff0d9dff.txt
```

### Ship it #3

After unpacking the docker image, I noticed that one of the layers deleted a file, so it must have been important. Just using files from previous layer:

```
    ./pickem ../4b642dec6bac2789e057c648477a087b.txt
```

### Thants #1

Just running `strings` on the file revealed the flag.

### Thants #2

Chunks could be seen with `pngchunk` program:

```sh
    pngcheck -c -v -t 02.png
```

I extracted it with a regexp and it contained a link. So I followed it a few times until finding a file without any more links:

```sh
    curl `ruby -e 'puts *STDIN.read.b.scan(/liNk((?:.*?)png)/)' < 02.png` > 02b.png
    curl `ruby -e 'puts *STDIN.read.b.scan(/liNk((?:.*?)png)/)' < 02b.png` > 02c.png
    curl `ruby -e 'puts *STDIN.read.b.scan(/liNk((?:.*?)png)/)' < 02c.png` > 02d.png
```

`pngcheck` revealed it had a suspicious looking `fuNk` chunk:

```
   chunk fuNk at offset 0x00025, length 97236
```

So I extracted it with `pry`:


```ruby
    d = open("02d.png", "rb", &:read)
    a = d[0x00025+4, 97233]
    open("02e", "wb").write(a)
```

It wasn't any meaningful format, but it contained a string of hex digits at the end, so I copied and pasted them and decoded with:

```ruby
    "digits here".scan(/../).map{|x| x.to_i(16).chr}.join
```

### Whitespace

Given a hint that it's a whitespace program I extracted it with Javascript console.

I tried running it in a whitespace interpretter, but it timed out.

So instead I used [interactive whitespace interpretter](https://vii5ard.github.io/whitespace/) to investigate the program. Looking at memory it was clear one of the function is calculating Fibonnaci numbers.

Those numbers were then passed to second function which seemed to calculate modulo operator. So I copied list of opcodes like:

```
    push 13
    call label_0
    push 131
    call label_1
    printc
    push 14
    call label_0
    push 269
    call label_1
    printc
    ...
```

Which translated to:

```ruby
    print (fib(13) % 131).chr
    print (fib(14) % 269).chr
    ...
```
