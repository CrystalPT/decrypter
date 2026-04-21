import hashlib
import sys
import os
import re

def identify_hash_type(hash_value):
    length = len(hash_value)
    is_hex = bool(re.match(r'^[a-f0-9]+$', hash_value))

    if hash_value.startswith('$2a$') or h.startswith('$2b$'):
        return 'bcrypt'
    if hash_value.startswith('$1$'):
        return "MD5-crypt"
    if hash_value.startswith('$6$'):
        return "SHA-512-crypt"

    if is_hex:
        if length == 32:
            return 'MD5'
        elif length == 40:
            return 'SHA1'
        elif length == 64:
            return 'SHA256'
        elif length == 128:
            return 'SHA512'
    if hash_value.endswith('='):
        return "Probably Base64 (not a hash!)"

    return "Unknown"

def crack_hash(target_hash, wordlist_path, hash_type):
    # try to crack the hash, use words from the txt file
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                
                if hash_type == "MD5":
                    hashed_password = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "SHA1":
                    hashed_password = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type == "SHA256":
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                else:
                    print(f"[-] Unsupported hash type: {hash_type}")
                    return None

                if hashed_password == target_hash:
                    return password
    except FileNotFoundError:
        print(f"[-] Wordlist not found: {wordlist_path}")
        return None
    except Exception as e:
        print(f"[-] Error: {e}")
        return None
    return None

def main():
    print("Python hash cracker")
    
    if len(sys.argv) > 1:
        target_hash = sys.argv[1]
    else:
        target_hash = input("Enter the hash to crack: ").strip()
    if len(sys.argv) > 2:
        wordlist_path = sys.argv[2]
    else:
        wordlist_path = input("Enter path to wordlist (default: wordlist.txt): ").strip()
        if not wordlist_path:
            wordlist_path = "wordlist.txt"

    print(f"\n[*] Analyzing hash: {target_hash}")
    hash_type = identify_hash_type(target_hash)
    print(f"[*] Identified Hash Type: {hash_type}")
    if hash_type == "Unknown":
        print("[-] Could not identify hash type. Supported: MD5, SHA1, SHA256.")
        # optional: Ask user to force a type or exit
        # exit to be safe
        return

    print(f"[*] Starting dictionary attack using {wordlist_path}...")
    found_password = crack_hash(target_hash, wordlist_path, hash_type)
    if found_password:
        print(f"\n[+] PASSWORD FOUND: {found_password}")
    else:
        print(f"\n[-] Password not found in wordlist.")

if __name__ == "__main__":
    main()
