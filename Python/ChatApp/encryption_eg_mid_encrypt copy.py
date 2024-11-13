import hashlib
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

def hash_base32_and_encrypt(input_string, secret_key):
    # Step 1: Hash the input string using SHA-256
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash.digest()  # Raw bytes of the hash
    print(hashed_string)

    # Step 2: Base32 encode the hashed string
    base32_encoded = base64.b32encode(hashed_string).decode('utf-8')
    print(base32_encoded)

    # Step 3: Ensure the secret_key is 32 bytes for AES-256
    key = hashlib.sha256(secret_key.encode()).digest()  # Create a 32-byte key from the secret_key
    print(key)

    # Step 4: Prepare the Base32 string for AES encryption (decode it to bytes)
    base32_bytes = base32_encoded.encode('utf-8')
    print(base32_bytes)

    # Step 5: Create AES cipher object in ECB mode (you can use other modes like CBC, but ECB is simpler)
    cipher = AES.new(key, AES.MODE_ECB)
    print(cipher)

    # Step 6: Pad the Base32 string to be a multiple of AES block size (16 bytes)
    padded_data = pad(base32_bytes, AES.block_size)
    print(padded_data)

    # Step 7: Encrypt the padded data
    encrypted_data = cipher.encrypt(padded_data)
    print(encrypted_data)

    # Step 8: Return the encrypted data in Base64 encoding for easier display
    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    print(encrypted_base64)

    return encrypted_base64

# Example usage
input_string = "HelloWorld"
secret_key = "this_is_a_very_secret_key"  # 32-byte key for AES-256

encrypted_string = hash_base32_and_encrypt(input_string, secret_key)
print(f"Encrypted String (AES-256): {encrypted_string}")
