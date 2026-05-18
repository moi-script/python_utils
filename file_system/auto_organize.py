import shutil
from pathlib import Path

def auto_organize_folder(directory_path):
    """
    Scans a folder and moves files into subfolders based on their category.
    """
    target_dir = Path(directory_path)
    
    # 1. Define our categories using a Dictionary mapping
    # We map specific file extensions to their new parent folder names
    categories = {
        'Images': {'.jpg', '.jpeg', '.png', '.gif', '.svg'},
        'Documents': {'.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.csv'},
        'Audio': {'.mp3', '.wav', '.flac'},
        'Video': {'.mp4', '.mkv', '.avi', '.mov'},
        'Archives': {'.zip', '.rar', '.tar', '.gz'}
    }
    
    # 2. Reverse the dictionary for lightning-fast lookups
    # This creates a map like: {'.jpg': 'Images', '.pdf': 'Documents'}
    extension_map = {}
    for folder_name, extensions in categories.items():
        for ext in extensions:
            extension_map[ext] = folder_name

    print(f"Scanning {target_dir} for files to organize...")
    
    # We use .iterdir() instead of .rglob() because we usually only want 
    # to organize the top level of a messy folder, not dig into existing subfolders.
    moved_count = 0
    for file_path in target_dir.iterdir():
        
        # We only want to move actual files, not the folders that are already there
        if file_path.is_file():
            
            # Get the extension in lowercase (e.g., '.JPG' becomes '.jpg')
            file_ext = file_path.suffix.lower()
            
            # Look up which folder this extension belongs to. 
            # If it's not in our list, default to a folder named 'Others'
            dest_folder_name = extension_map.get(file_ext, 'Others')
            
            # Create the full path for the new destination folder
            dest_folder_path = target_dir / dest_folder_name
            
            # 3. Create the folder if it doesn't exist yet
            dest_folder_path.mkdir(exist_ok=True)
            
            # Define exactly where the file will land
            dest_file_path = dest_folder_path / file_path.name
            
            # 4. Move the file
            try:
                # Safety check: Don't overwrite a file if it already exists in the destination
                if not dest_file_path.exists():
                    shutil.move(str(file_path), str(dest_file_path))
                    print(f"Moved: {file_path.name} -> {dest_folder_name}/")
                    moved_count += 1
                else:
                    print(f"Skipped: {file_path.name} (File already exists in destination)")
            except PermissionError:
                print(f"Error: Could not move {file_path.name} (File might be open in another program)")

    print(f"\nOrganization complete! Moved {moved_count} files.")

# Example usage:
# auto_organize_folder("/Users/YourName/Downloads")