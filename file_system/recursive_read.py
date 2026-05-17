
from pathlib import Path
import os
import concurrent.futures


# single thread file read



def process_files_recursively(directory_path, pattern="*"):
    """
    Recursively finds and reads files.
    Use pattern="*.txt" to only read text files, for example.
    """
    target_dir = Path(directory_path)
    print(f"Target dir :: {target_dir}")
    
    # .rglob() yields a generator of Path objects
    for file_path in target_dir.rglob(pattern):
        print(f"File path {file_path}")
        
        # rglob grabs directories too, so we ensure it's a file
        if file_path.is_file():
            try:
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as file: # auto close / clean
                    content = file.read()
                    # print(f"Read {file_path.name} ({len(content)} characters)")
                    # print(f"file path :: {file_path} :: content :: {content}")
                    
                    # Do something with 'content' here\
                    
            except PermissionError:
                print(f"Skipped {file_path.name}: Permission Denied")
            except UnicodeDecodeError:
                print(f"Skipped {file_path.name}: Not a UTF-8 text file")

# Example usage:
# process_files_recursively("./trash", "*.txt")


#pathlib -> this organise  the messy path of hardrive
#rglob() -> this acts as the file_path recurisive finder
#is_file() -> if the name of file had something like  . is it like  a valid file  name 
# PermissionError -> Os throw  an error, if we dont have enough permission for that file 
# UnicodeDecodeError - this translate into binary, if  we have file that cannot be parse with text, this helps 



def classic_recursive_reader(directory_path):
    # os.walk yields a 3-tuple for every directory it visits
    for root, dirs, files in os.walk(directory_path): 
        
        # Optional: Exclude hidden directories (like .git) from being searched
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file_name in files:
            # Combine the path safely
            full_path = os.path.join(root, file_name)
            
            # Example filter: only read .csv files
            if full_path.endswith('.csv'):
                print(f"Found CSV: {full_path}")
                # Add your reading logic here
            else :
                print('Txt found :', full_path)
                


# classic_recursive_reader('./trash')

# os.walk() -> root, dirs, files this easily fetch some root, dir and filename so we dont hhave to check if file is valid
# endswith() -> string method to check if it ends with this char
# startswith()  -> string method to chekc if it start with this  char
# dirs[:] -> In-place List Modification




# multi thread 

def read_single_file(file_path):
    """
    Worker function: This executes on a single thread.
    It handles reading and processing exactly one file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # --- Insert your actual data processing logic here ---
            # For demonstration, we just count the characters.
            char_count = len(content)
            
            # Return the result back to the main thread
            return f"SUCCESS: {file_path.name} ({char_count} chars)"
            
    except PermissionError:
        return f"SKIPPED: {file_path.name} (Permission Denied)"
    except UnicodeDecodeError:
        return f"SKIPPED: {file_path.name} (Not a UTF-8 text file)"
    except Exception as e:
        return f"ERROR: {file_path.name} ({str(e)})"

def process_files_concurrently(directory_path, pattern="*", max_threads=10):
    """
    Orchestrator function: Finds files and distributes them to the thread pool.
    """
    target_dir = Path(directory_path)
    
    # 1. Gather all target files first
    # Using a list comprehension ensures we only pass actual files to our threads
    files_to_process = [p for p in target_dir.rglob(pattern) if p.is_file()]
    
    print(f"Found {len(files_to_process)} files. Starting thread pool...")
    
    successful_reads = 0

    # 2. Spin up the Thread Pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        
        # Submit tasks to the pool. We use a dictionary to map the 'Future' 
        # (the pending task) back to the original file path.
        future_to_file = {
            executor.submit(read_single_file, path): path 
            for path in files_to_process
        }
        
        # print(f"Future_to_file : {future_to_file}")
        
        # 3. Harvest the results as soon as they finish
        # as_completed yields futures as they finish, regardless of the order they were submitted
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                # .result() gives us whatever read_single_file() returned
                result_message = future.result()
                print(result_message)
                
                if result_message.startswith("SUCCESS"):
                    successful_reads += 1
                    
            except Exception as exc:
                # Catch any catastrophic thread crashes
                print(f"CRITICAL ERROR: {file_path.name} generated an exception: {exc}")

    print(f"\nFinished! Successfully processed {successful_reads} out of {len(files_to_process)} files.")

# Example usage:
process_files_concurrently("./trash", pattern="*.txt", max_threads=8)



# concurrent.futures.ThreadPoolExecutor
# future_to_file
# future_to_file = {
#     executor.submit(read_single_file, path): path 
#     for path in files_to_process
# }

