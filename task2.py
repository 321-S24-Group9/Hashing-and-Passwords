import time
import itertools
import bcrypt

# Function to parse the hash string and extract algorithm, workfactor, salt, and hash
def parse_hash(hash_string):
    parts = hash_string.split('$')
    algorithm = parts[1]
    workfactor = parts[2]
    salt_hash = parts[3]
    salt_length = 22  # Length of the salt in base64 encoding
    salt = salt_hash[:salt_length]
    password_hash = salt_hash[salt_length:]
    return algorithm, workfactor, salt, password_hash

# Function to load users from the file
def load_users(filename):
    users = []
    with open(filename, 'r') as file:
        for line in file:
            username, hash_string = line.strip().split(':')
            algorithm, workfactor, salt, password_hash = parse_hash(hash_string)
            users.append((username, algorithm, workfactor, salt, password_hash))
    return users

# Function to generate potential passwords
def generate_passwords():
    password_lengths = range(6, 11)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for length in password_lengths:
        for password in itertools.product(alphabet, repeat=length):
            yield ''.join(password)

# Function to crack passwords
def crack_passwords(users):
    cracked_passwords = []
    start_time = time.time()
    
    for username, algorithm, workfactor, salt, password_hash in users:
        print(f"Cracking password for user: {username}")
        
        for password in generate_passwords():
            # Generate bcrypt hash with the same salt and work factor
            test_hash = bcrypt.hashpw(password.encode('utf-8'), f"${algorithm}${workfactor}${salt}".encode('utf-8')).decode('utf-8')
            if test_hash == f"${algorithm}${workfactor}${salt}${password_hash}":
                end_time = time.time()
                crack_time = end_time - start_time
                cracked_passwords.append((username, password, crack_time))
                print(f"Password for user {username} cracked: {password}")
                break
    
    return cracked_passwords

if __name__ == "__main__":
    filename = 'shadow.txt'
    users = load_users(filename)
    cracked_passwords = crack_passwords(users)
    
    # Write cracked passwords to a file
    with open('cracked_passwords.txt', 'w') as file:
        for username, password, crack_time in cracked_passwords:
            file.write(f"User: {username}, Password: {password}, Time to crack: {crack_time} seconds\n")

    print("Cracked passwords saved to 'cracked_passwords.txt'")
