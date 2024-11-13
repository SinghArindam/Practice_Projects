from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import base64
import hashlib

def decrypt_base32_and_hash(encrypted_base64_string, secret_key):
    # Step 1: Base64 decode the encrypted string to get the raw encrypted data
    encrypted_data = base64.b64decode(encrypted_base64_string)
    print("Encrypted Data (Base64 decoded):", encrypted_data)

    # Step 2: Ensure the secret_key is 32 bytes for AES-256
    key = hashlib.sha256(secret_key.encode()).digest()  # Create a 32-byte key from the secret_key
    print("AES Key (32 bytes):", key)

    # Step 3: Create AES cipher object in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    print("Cipher Object:", cipher)

    # Step 4: Decrypt the encrypted data
    decrypted_data = cipher.decrypt(encrypted_data)
    print("Decrypted Data (with padding):", decrypted_data)

    # Step 5: Check if the decrypted data has padding
    try:
        # Try to unpad the decrypted data
        unpadded_data = unpad(decrypted_data, AES.block_size)
        print("Unpadded Decrypted Data:", unpadded_data)
    except ValueError as e:
        print(f"Error during unpadding: {e}")
        return None

    # Step 6: Base32 decode the unpadded data to get the original hash
    try:
        base32_decoded = base64.b32decode(unpadded_data).decode('utf-8')
        print("Base32 Decoded (original hash):", base32_decoded)
    except Exception as e:
        print(f"Error during Base32 decoding: {e}")
        return None

    # Step 7: Return the original hash as a string
    return base32_decoded

# Example usage:
encrypted_string = "2p3PST8rRYWJbRY35DdWhUuFZY4DncY6Q2k/4RnRMecEx9iFGMGvJ869nZK01qd0JaAxB2sYAv/BrpG6cIhZrg=="  # The Base64 encoded encrypted string you got from the encryption function
secret_key = "this_is_a_very_secret_key'"  # Same secret key used during encryption

decrypted_string = decrypt_base32_and_hash(encrypted_string, secret_key)
if decrypted_string:
    print(f"Decrypted String (SHA-256 hash): {decrypted_string}")
else:
    print("Decryption failed.")



decrypted_string = decrypt_base32_and_hash(encrypted_string, secret_key)
print(f"Decrypted String (SHA-256 hash): {decrypted_string}")