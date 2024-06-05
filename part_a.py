import hashlib

def hash_input(input_string):
    # Create a new sha256 hash object
    sha256_hash = hashlib.sha256()
    
    # Update the hash object with the bytes of the input string
    sha256_hash.update(input_string.encode('utf-8'))
    
    # Get the hexadecimal digest of the hash
    hex_digest = sha256_hash.hexdigest()
    
    return hex_digest

if __name__ == "__main__":
    # Get user input
    input_string = input("Enter the string to hash: ")
    
    # Compute the SHA-256 hash
    hash_result = hash_input(input_string)
    
    # Print the result
    print(f"SHA-256 hash of '{input_string}': {hash_result}")
