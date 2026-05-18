import string

# strip() " data ".strip() → "data"
# lower() "SQL".lower() → "sql"
# upper()
# startsWith()   "test.py".startswith("test") → True
# endsWith()     "data.csv".endswith(".csv") → True
# isdigit()     "12345".isdigit() → True
# zfill(width)      "42".zfill(4) → "0042"





def string_to_list (strs : str) : 
    return strs.split(",")

def list_to_str(data : list) -> list :
    return  " ".join(data)

def swap_string(data : str, strFind : str, strToSwap) :
    return data.lower().replace(strFind, strToSwap)


def get_str_ascii() :
    return string.ascii_letters

def get_str_digits() :
    return string.digits

def get_str_punctuation() :
    return string.punctuation

def remove_punctaution(dirty_word : str) :
    return "".join(char for char in dirty_word if char not in string.punctuation)
# Example Use Case: Stripping all punctuation from a word
# Result: "Hello"


