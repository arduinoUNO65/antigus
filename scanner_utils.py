# scanner_utils.py
# Utility functions for file scanning and threat detection
import hashlib

# Example: Calculate SHA256 hash of a file

def file_hash(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

# Example: Check file against a list of known bad hashes

def is_malicious(path, bad_hashes):
    h = file_hash(path)
    return h in bad_hashes if h else False
