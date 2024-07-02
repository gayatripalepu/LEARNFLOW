import os
import json
import base64
import getpass
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# File to store encrypted credentials
CREDENTIALS_FILE = "credentials.json"

# Key and IV for encryption (should be stored securely in a real application)
ENCRYPTION_KEY = base64.urlsafe_b64encode(secrets.token_bytes(32))
INITIALIZATION_VECTOR = secrets.token_bytes(16)

def create_strong_password(length=16):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
    return ''.join(secrets.choice(charset) for _ in range(length))

def encode_data(plaintext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.urlsafe_b64encode(ciphertext).decode()

def decode_data(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    padded_data = decryptor.update(base64.urlsafe_b64decode(ciphertext)) + decryptor.finalize()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext.decode()

def read_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

def store_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file, indent=4)

def save_password(category, service, username, password):
    credentials = read_credentials()
    if category not in credentials:
        credentials[category] = {}
    encrypted_password = encode_data(password, ENCRYPTION_KEY, INITIALIZATION_VECTOR)
    credentials[category][service] = {"username": username, "password": encrypted_password}
    store_credentials(credentials)
    print(f"Password for {service} saved successfully under {category} category.")

def get_password(category, service):
    credentials = read_credentials()
    if category in credentials and service in credentials[category]:
        encrypted_password = credentials[category][service]["password"]
        username = credentials[category][service]["username"]
        decrypted_password = decode_data(encrypted_password, ENCRYPTION_KEY, INITIALIZATION_VECTOR)
        return username, decrypted_password
    else:
        print(f"No password found for {service} under {category} category.")
        return None, None

def run_password_manager():
    while True:
        print("\nPassword Manager")
        print("1. Save a new password")
        print("2. Get a saved password")
        print("3. Create a strong password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            category = input("Enter the category: ")
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = getpass.getpass("Enter the password: ")
            save_password(category, service, username, password)

        elif choice == "2":
            category = input("Enter the category: ")
            service = input("Enter the service name: ")
            username, password = get_password(category, service)
            if username and password:
                print(f"Username: {username}\nPassword: {password}")

        elif choice == "3":
            length = int(input("Enter the desired length for the password: "))
            print("Generated password: ", create_strong_password(length))

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    run_password_manager()
