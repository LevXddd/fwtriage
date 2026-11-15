import sys
from math import log
SIGNATURES = {

    b"\x7FELF":      "ELF executable",
    b"PK\x03\x04":   "ZIP archive",
    b"\x1f\x8b":     "gzip compressed",
    b"\x89PNG":      "PNG image",
    b"%PDF":         "PDF document",
    b"\xff\xd8\xff": "JPEG image", 
        }
    
def detect_filetype(data):
    for signature, name in SIGNATURES.items():
        if data.startswith(signature):
            return name
    else:
        return "unknown"

def extract_strings(data, min_len = 4):
    results= []
    current = ""
    for byte in data:
        if 32 <= byte <= 126: # IN ASCII, FROM 32 TO 126 ARE PRINTABLE CHARACTERS, WHILE OTHERS ARE USUALLY AN INSTRUCTION FOR THE PC
            current += chr(byte) # chr(byte) converts the byte to a character
        else:
            if len(current) >= min_len:
                results.append(current)
            current = ""
    if len(current) >= min_len:
       results.append(current) # Again, why? imagine we have like %PDF\HELLO", it will stop after 0 and will not add the "HELLO" string, so we need to add one more, that is our purpose.
    return results


def main():
    try:
        if len(sys.argv) < 2 or len(sys.argv) > 2:
           sys.exit("Incorrect")
        with open(sys.argv[1], "rb") as file:
            data = file.read()
    except FileNotFoundError:
        sys.exit("File is not found")
    else: 
        print(f"File type: {detect_filetype(data)}")
        print("Extracted strings:")
        for letter in extract_strings(data):
            print(" ", letter)
        print(f"Entropy of the file: {calculate_the_entropy(data):.2f} ")
        

def calculate_the_entropy(name):
    probability_sum = 0   
     # first of all, we have formula like - sigma p(x) * log 2 p(x)
    # x is just a variable, like if we have AAAA, then x will be A, but we should transfer this to a number.
    p = 0
    total = 0
    counts = {}
    for letter in name:
        if letter in counts:
            counts[letter] += 1 # we are just adding value
        else:
            counts[letter] = 1

    for i in counts:
        p = counts[i] / len(name)
        total += -1 * p * log(p, 2)
    return total










if __name__ == "__main__":
    main()
   

   


    