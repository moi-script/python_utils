import hashlib
from pathlib import Path
from collections import defaultdict

def get_file_hash(file_path, chunk_size=8192):
    file_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            file_hash.update(chunk)
    return file_hash.hexdigest()

def find_duplicates_by_extension(directory_path, target_extensions=None):
    """
    Finds duplicate files, optionally filtering by extension.
    Example target_extensions: {'.jpg', '.jpeg', '.png'}
    """
    target_dir = Path(directory_path)
    
    # PRO TRICK 1: Normalize the target extensions
    # Convert them all to lowercase and ensure they are a 'set' for lightning-fast lookups
    if target_extensions:
        target_extensions = {ext.lower() for ext in target_extensions}
    
    files_by_size = defaultdict(list)
    
    print(f"Step 1: Scanning file sizes in {directory_path}...")
    for file_path in target_dir.rglob('*'):
        if file_path.is_file():
            
            # PRO TRICK 2: The Extension Filter
            if target_extensions:
                # .suffix grabs the extension (e.g., '.JPG')
                # .lower() ensures '.JPG' matches '.jpg' in our target set
                if file_path.suffix.lower() not in target_extensions:
                    continue # Skip to the next file in the loop
            
            try:
                size = file_path.stat().st_size
                files_by_size[size].append(file_path)
            except PermissionError:
                pass

    duplicates = defaultdict(list)
    
    print("Step 2: Hashing potential duplicates...")
    for size, file_paths in files_by_size.items():
        if len(file_paths) < 2:
            continue
            
        for file_path in file_paths:
            try:
                file_hash = get_file_hash(file_path)
                duplicates[file_hash].append(file_path)
            except PermissionError:
                pass

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
# Find ONLY duplicate images
# find_duplicates_by_extension("./my_photos", target_extensions={'.jpg', '.png', '.jpeg'})