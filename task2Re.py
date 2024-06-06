import bcrypt
import time
from nltk.corpus import words

# Load the NLTK words corpus
word_list = words.words()

# Filter words to be between 6 and 10 letters long
filtered_words = [word for word in word_list if 6 <= len(word) <= 10]

def parse_shadow_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    user_hash_data = []
    for line in lines:
        user, hash_data = line.strip().split(':', 1)
        user_hash_data.append((user, hash_data))
    return user_hash_data

def crack_password(user, full_hash, word_list):
    # Extract salt (first 29 characters)
    salt = full_hash[:29]
    for word in word_list:
        if bcrypt.checkpw(word.encode(), full_hash.encode()):
            return word
    return None

def main():
    shadow_file = 'shadow_part.txt'
    user_hash_data = parse_shadow_file(shadow_file)

    results = []

    for user, full_hash in user_hash_data:
        print(f"Cracking password for user: {user}")
        start_time = time.time()
        password = crack_password(user, full_hash, filtered_words)
        end_time = time.time()
        elapsed_time_minutes = (end_time - start_time) / 60  # Convert to minutes
        results.append((user, password, elapsed_time_minutes))
        print(f"Password for user {user} is: {password}")
        print(f"Time taken: {elapsed_time_minutes:.2f} minutes")

    # Write results to a text file
    with open('cracked_passwords.txt', 'w') as file:
        file.write("User\tPassword\tTime (minutes)\n")
        for result in results:
            user, password, elapsed_time_minutes = result
            file.write(f"{user}\t{password}\t{elapsed_time_minutes:.2f}\n")

if __name__ == "__main__":
    main()
