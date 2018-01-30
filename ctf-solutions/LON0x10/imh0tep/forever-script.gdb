set width 0
set height 0
set verbose off

b *0x400ae4
commands 1
  silent
  set *(char*)($rbp-9)=1
  c
end

b *0x400c1d
commands 2
  silent
  set $eax=0
  c
end

b *0x400a6c
commands 3
  silent
  set $al=0x2a
  c
end

r