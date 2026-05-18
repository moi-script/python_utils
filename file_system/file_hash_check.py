import hashlib
from pathlib import Path

def verify_file_hash(file_path, expected_hash, algorithm="sha256", chunk_size=8192):
    """
    Computes the hash of a file and compares it against an expected hash.
    """
    target_file = Path(file_path)
    
    # 1. Check if the file actually exists
    if not target_file.is_file():
        print(f"[ERROR] File not found: {target_file}")
        return False
        
    print(f"Calculating {algorithm.upper()} hash for {target_file.name}...")

    try:
        # 2. Dynamically load the requested hash algorithm
        # This allows the user to pass "md5", "sha1", "sha256", etc.
        hasher = hashlib.new(algorithm.lower())
    except ValueError:
        print(f"[ERROR] Unsupported hash algorithm: {algorithm}")
        return False

    # 3. Read the file in chunks to save RAM
    try:
        with open(target_file, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
    except PermissionError:
        print(f"[ERROR] Permission denied: Cannot read {target_file.name}")
        return False

    # 4. Finalize the hash calculation
    calculated_hash = hasher.hexdigest()
    
    # 5. Clean up the expected hash for a fair comparison
    # We strip whitespace and convert both to lowercase
    expected_clean = expected_hash.strip().lower()
    
    print("-" * 40)
    print(f"Expected:   {expected_clean}")
    print(f"Calculated: {calculated_hash}")
    
    # 6. The Verdict
    if calculated_hash == expected_clean:
        print("\n✅ MATCH! The file is perfectly intact.")
        return True
    else:
        print("\n❌ MISMATCH! The file is corrupted or tampered with.")
        return False

# Example Usage:
# Imagine you downloaded 'ubuntu.iso' and the website said the SHA-256 hash is:
# "e2b023e1f0e8f72c2957eb6a6d6e1fae923e3e18a99477eb71190bc1f19f6a5"

# verify_file_hash(
#     file_path="./ubuntu.iso", 
#     expected_hash="e2b023e1f0e8f72c2957eb6a6d6e1fae923e3e18a99477eb71190bc1f19f6a5",
#     algorithm="sha256"
# )