from pathlib import Path

def batch_rename_files(directory_path, prefix="File", target_extension=None, dry_run=True):
    """
    Renames files in a directory sequentially (e.g., File_001.jpg, File_002.jpg).
    """
    target_dir = Path(directory_path)
    
    if dry_run:
        print("\n=== DRY RUN MODE: No files will actually be renamed ===")
    else:
        print("\n=== DANGER: ACTUALLY RENAMING FILES ===")

    # 1. Gather and sort the files
    # Sorting ensures that File 1 and File 2 don't get randomly swapped
    files_to_rename = []
    for file_path in target_dir.iterdir():
        if file_path.is_file():
            # If an extension is specified, only grab those files
            if target_extension:
                if file_path.suffix.lower() == target_extension.lower():
                    files_to_rename.append(file_path)
            else:
                files_to_rename.append(file_path)
                
    files_to_rename.sort()

    if not files_to_rename:
        print("No matching files found to rename.")
        return

    # 2. Loop through and rename
    # enumerate(..., start=1) makes our counter start at 1 instead of 0
    for index, file_path in enumerate(files_to_rename, start=1):
        
        # Keep the original extension
        extension = file_path.suffix.lower()
        
        # 3. Format the new name with padded zeros (e.g., "001" instead of "1")
        new_name = f"{prefix}_{index:03d}{extension}"
        
        # 4. Safely construct the new full path
        new_file_path = file_path.with_name(new_name)
        
        # Prevent overwriting an existing file by accident
        if new_file_path.exists() and new_file_path != file_path:
             print(f"  [SKIPPED] Cannot rename to {new_name} (File already exists)")
             continue

        if dry_run:
            print(f"  [WOULD RENAME]  {file_path.name}  ->  {new_name}")
        else:
            try:
                # 5. The actual rename execution
                file_path.rename(new_file_path)
                print(f"  [RENAMED]       {file_path.name}  ->  {new_name}")
            except PermissionError:
                print(f"  [ERROR] Permission Denied: Could not rename {file_path.name}")

    if not dry_run:
        print(f"\nSuccessfully renamed {len(files_to_rename)} files.")

# Example usage:
# batch_rename_files("./vacation_photos", prefix="Hawaii", target_extension=".jpg", dry_run=True)