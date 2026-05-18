from pathlib import Path

def safely_delete_duplicates(duplicates_dict, dry_run=True):
    """
    Takes a dictionary of duplicates, keeps the first file, and deletes the rest.
    Set dry_run=False to actually delete the files.
    """
    if dry_run:
        print("\n=== DRY RUN MODE: No files will actually be deleted ===")
    else:
        print("\n=== DANGER: ACTUALLY DELETING FILES ===")

    freed_space_bytes = 0
    deleted_count = 0

    # Iterate through our dictionary of found duplicates
    for file_hash, file_paths in duplicates_dict.items():
        
        # We only care if there is more than 1 file with the same hash
        if len(file_paths) > 1:
            
            # 1. The Keep-One Logic
            # We assign the first file in the list as our "Original"
            original_file = file_paths[0]
            
            # We grab everything EXCEPT the first file to be deleted
            duplicates_to_delete = file_paths[1:]
            
            print(f"\n[KEEPING]  {original_file}")

            for duplicate in duplicates_to_delete:
                # Calculate how much space we are saving
                file_size = duplicate.stat().st_size
                
                if dry_run:
                    # 2. The Dry Run
                    print(f"  [WOULD DELETE]  {duplicate} ({file_size / 1024 / 1024:.2f} MB)")
                else:
                    try:
                        # 3. The actual deletion
                        duplicate.unlink() 
                        print(f"  [DELETED]       {duplicate}")
                        
                        freed_space_bytes += file_size
                        deleted_count += 1
                        
                    except PermissionError:
                        print(f"  [ERROR] Permission Denied: Could not delete {duplicate.name}")
                    except FileNotFoundError:
                        print(f"  [ERROR] File disappeared before we could delete it: {duplicate.name}")

    if not dry_run:
        saved_mb = freed_space_bytes / (1024 * 1024)
        print(f"\nCleanup Complete! Deleted {deleted_count} files and freed {saved_mb:.2f} MB of space.")

# Example usage (assuming 'duplicates' is the dictionary from our previous script):
# Step 1: Test it safely first
# safely_delete_duplicates(duplicates, dry_run=True)

# Step 2: Once you review the output and agree, run it for real
# safely_delete_duplicates(duplicates, dry_run=False)