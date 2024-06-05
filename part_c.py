import hashlib
import random
import string
import time
import csv

def hash_input_truncated(input_string, bits):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    full_hex_digest = sha256_hash.hexdigest()
    full_int_digest = int(full_hex_digest, 16)
    truncated_int_digest = full_int_digest & ((1 << bits) - 1)
    return truncated_int_digest

def find_collision(bits):
    hash_dict = {}
    attempts = 0
    start_time = time.time()

    while True:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        truncated_hash = hash_input_truncated(random_string, bits)

        if truncated_hash in hash_dict:
            end_time = time.time()
            execution_time_ms = (end_time - start_time) * 1000
            return attempts, execution_time_ms

        hash_dict[truncated_hash] = random_string
        attempts += 1

def main():
    results = []

    for bits in range(8, 51, 2):
        attempts, execution_time_ms = find_collision(bits)
        results.append((bits, attempts, execution_time_ms))

    with open('collision_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Bits', 'Attempts', 'Execution Time (ms)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow({'Bits': result[0], 'Attempts': result[1], 'Execution Time (ms)': result[2]})

if __name__ == "__main__":
    main()