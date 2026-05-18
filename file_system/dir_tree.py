from pathlib import Path

def print_directory_tree(directory_path, prefix="", max_depth=3, current_depth=1):
    """
    Recursively prints a visual tree of a directory.
    max_depth prevents the script from freezing on massive drives (like C:/).
    """
    # 1. Safety valve: stop digging if we've gone too deep
    if current_depth > max_depth:
        return

    target_dir = Path(directory_path)
    
    try:
        # 2. Gather contents and sort them (Folders first, then files alphabetically)
        # We use a custom sorting key to achieve this.
        items = list(target_dir.iterdir())
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
        
    except PermissionError:
        print(f"{prefix}└── [Access Denied]")
        return
        
    total_items = len(items)
    
    for index, item in enumerate(items):
        # 3. Are we on the very last item in this folder?
        is_last_item = (index == total_items - 1)
        
        # 4. Choose the right branch symbol
        branch = "└── " if is_last_item else "├── "
        
        # Print the current item
        print(f"{prefix}{branch}{item.name}")
        
        # 5. The Recursion Step: If it's a folder, dive inside!
        if item.is_dir():
            # If this folder is the last item, its children just get blank spaces.
            # If it's NOT the last item, its children need a vertical line "│" connecting 
            # this folder to the folders below it.
            extension = "    " if is_last_item else "│   "
            
            # The function calls ITSELF with the new, longer prefix
            print_directory_tree(
                item, 
                prefix=prefix + extension, 
                max_depth=max_depth, 
                current_depth=current_depth + 1
            )

# Example Usage:
# Print the starting folder name first, then generate the tree
# start_path = Path("./my_project")
# print(f"📁 {start_path.name}/")
# print_directory_tree(start_path, max_depth=3)