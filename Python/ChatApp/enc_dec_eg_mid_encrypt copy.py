import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_mid(password):
    # Step 1: Hash the password (optional, but you can hash before encryption)
    hashed_password = hash_string(password)
    print(f"Hashed password : {hashed_password.hex()}")

    # Step 2: Encode the hash using Base64
    encoded_hash = base64_encode(hashed_password)
    print(f"Encoded Hashed Password: {encoded_hash}")

    # Step 3: Encrypt the Base64 encoded hash with AES-256
    key = get_random_bytes(32)  # AES-256 key must be 32 bytes
    iv, encrypted_password = aes_encrypt(encoded_hash, key)
    print(f"Encrypted Password (Base64): {encrypted_password}")
    print(f"IV (Base64): {iv}")
    return [iv, encrypted_password, key]

def decrypt_mid(enc_data):
    iv, encrypted_password, key = enc_data[0],enc_data[1],enc_data[2]
    # Step 4: Decrypt the AES encrypted password
    decrypted_password = aes_decrypt(encrypted_password, iv, key)
    print(f"Decrypted Password: {decrypted_password}")

    # Step 5: Decode the Base64 encrypted hash to get the original hash (optional step)
    decoded_hash = base64_decode(decrypted_password.encode('utf-8'))
    print(f"Decoded Hashed Password: {decoded_hash.hex()}")
    return decoded_hash.hex()

def hash_string(input_string):
    """ Hash the input string using SHA-256. """
    sha256_hash = hashlib.sha256(input_string.encode('utf-8'))
    return sha256_hash.digest()

def base64_encode(data):
    """ Encode the data in base64. """
    return base64.b64encode(data).decode('utf-8')

def base64_decode(data):
    """ Decode base64 encoded data. """
    return base64.b64decode(data)

def aes_encrypt(data, key):
    """ Encrypt data using AES-256. """
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')  # Encode IV for transmission
    encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    return iv, encrypted_data_base64

def aes_decrypt(encrypted_data_base64, iv_base64, key):
    """ Decrypt data using AES-256. """
    iv = base64.b64decode(iv_base64)
    encrypted_data = base64.b64decode(encrypted_data_base64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')


# Example Usage: Encrypt and Decrypt Password
password = "my_secure_password"
enc_data = encrypt_mid(password)
# print(enc_data)
decrypt_mid(enc_data)