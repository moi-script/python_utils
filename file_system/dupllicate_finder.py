import hashlib
from pathlib import Path
from collections import defaultdict

def get_file_hash(file_path, chunk_size=8192):
    """
    Reads a file in small chunks and generates a SHA-256 hash.
    Reading in chunks prevents running out of RAM on massive files.
    """
    # We use SHA-256 for a highly accurate fingerprint
    file_hash = hashlib.sha256()
    
    # Notice the 'rb' (read binary) - we must read raw bytes, not text
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break # We reached the end of the file
            file_hash.update(chunk)
            
    return file_hash.hexdigest()

def find_duplicates(directory_path):
    target_dir = Path(directory_path)
    
    # Step 1: Group files by their size
    # defaultdict creates a new list automatically if the size isn't in the dictionary yet
    files_by_size = defaultdict(list)
    
    print("Step 1: Scanning file sizes...")
    for file_path in target_dir.rglob('*'):
        if file_path.is_file():
            try:
                # .stat().st_size gets the file size in bytes without opening the file!
                size = file_path.stat().st_size
                files_by_size[size].append(file_path)
            except PermissionError:
                pass # Skip files we can't access

    # Step 2: Only hash files that share a size with another file
    duplicates = defaultdict(list)
    
    print("Step 2: Hashing potential duplicates...")
    for size, file_paths in files_by_size.items():
        # If there's only 1 file with this size, it's not a duplicate. Skip it.
        if len(file_paths) < 2:
            continue
            
        # If we have multiple files with the same size, calculate their hashes
        for file_path in file_paths:
            try:
                file_hash = get_file_hash(file_path)
                duplicates[file_hash].append(file_path)
            except PermissionError:
                pass

    # Step 3: Print the results
    found_dupes = False
    for file_hash, file_paths in duplicates.items():
        if len(file_paths) > 1:
            found_dupes = True
            print(f"\nFound {len(file_paths)} identical files (Hash: {file_hash[:8]}...):")
            for path in file_paths:
                print(f"  - {path}")
                
    if not found_dupes:
        print("\nNo duplicates found!")



# Example usage:
# find_duplicates("./my_folder")