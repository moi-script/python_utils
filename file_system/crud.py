import os
import shutil

# open a file open(filename, readmode) 

# "r" - Read - Default value. Opens a file for reading, error if the file does not exist
# "a" - Append - Opens a file for appending, creates the file if it does not exist
# "w" - Write - Opens a file for writing, creates the file if it does not exist
# "x" - Create - Creates the specified file, returns an error if the file exists

# "t" - Text - Default value. Text mode
# "b" - Binary - Binary mode (e.g. images)
# default


fileName = 'files/test.txt'
def openFile(file_name : str, read_mode) :
    global file_content
    file_content =  open(file_name, read_mode)
    print(file_content.read())
    
# rt -> reading text | rb -> reading binary
# openFile(fileName, 'rb')




def manual_close_open(file_name : str, read_mode : str) :
    o = open(file_name, read_mode)
    print(o.readline()) # reading a first line of file
    o.close()



# auto_clean_open(fileName, 'rt')

def close_running_file(file_name : str,  read_mode : str) : 
    if file_content.close :
        print('File is still open, we are closing it now')
        return file_content.close()
        
    if file_content.close :
        print("Successfully closed the file")
    

# close_running_file(fileName, 'rb')


# best practice
def auto_clean_open(file_name : str, read_mode : str) :
    with open(file_name, read_mode) as f:
        print(f.read())
        
        
def test_read_file(file_name : str, read_mode : str) -> str :
    with open(file_name, read_mode) as f :
        print(f.readline()) 
        print(f.readline())
        
# test_read_file(fileName, 'rt')
        
def read_file_loop(file_name : str, read_mode : str) :
    with open(file_name, read_mode) as f :
        for x in f :
            print(x)

# read_file_loop(fileName, 'rt')




# write to existing file 


def writeTestFile(file_name : str, read_mode : str, content : any) : 
    
    with open(file_name, read_mode) as f :
        f.write(content)
    
    with open(file_name, 'rt') as f:
        print(f.read())    
        

# writeTestFile(fileName, 'a', "new hello world 3 \n") # a -> append


def createFile(file_name : str) :
    with open(file_name, 'x') as f :
        return f

# print(createFile('hello.txt').close)        
        
    



def deleteFile(file_name : str) :
    if "." not in file_name : # check if file name is valid
        print("File not valid")
        
    if os.path.exists(file_name)  and '.' in file_name :
        os.remove(file_name) 
    else :
        print("File does not exist")

# deleteFile(fileName)

def deleteFolder(folder_name : str) :
    if os.path.exists(folder_name) :  
        os.rmdir(folder_name) 
             
# deleteFolder('files')             


# implementing to recycle bin and some backups

def backFileBin(file_name: str):
    if not os.path.exists(file_name):
        print("File or folder does not exist")
        return

    # Ensure trash folder exists
    os.makedirs("trash", exist_ok=True)

    # Get only the base filename (avoid nested paths issue)
    base_name = os.path.basename(file_name)

    destination = os.path.join("trash", base_name)

    shutil.move(file_name, destination)
    print(f"Moved '{file_name}' -> '{destination}'")

backFileBin('files/hello.txt')