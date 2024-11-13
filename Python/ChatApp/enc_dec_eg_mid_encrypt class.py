import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class Encryptor:
    def __init__(self):
        # Generate a random AES-256 key for the instance
        self.key = get_random_bytes(32)  # AES-256 requires a 32-byte key
    
    def encrypt(self, password):
        """Hashes, encodes, and encrypts the password."""
        hashed_password = self._hash_string(password)
        print(f"Hashed Password (Hex): {hashed_password.hex()}")
        
        encoded_hash = self._base64_encode(hashed_password)
        print(f"Encoded Hashed Password: {encoded_hash}")
        
        iv, encrypted_password = self._aes_encrypt(encoded_hash)
        print(f"Encrypted Password (Base64): {encrypted_password}")
        print(f"IV (Base64): {iv}")
        
        return [iv, encrypted_password, self.key]
    
    def decrypt(self, iv, encrypted_password):
        """Decrypts and decodes the password."""
        decrypted_password = self._aes_decrypt(encrypted_password, iv)
        print(f"Decrypted Password: {decrypted_password}")
        
        decoded_hash = self._base64_decode(decrypted_password.encode('utf-8'))
        print(f"Decoded Hashed Password (Hex): {decoded_hash.hex()}")
        return decoded_hash.hex()

    def _hash_string(self, input_string):
        """Hashes the input string using SHA-256."""
        return hashlib.sha256(input_string.encode('utf-8')).digest()

    def _base64_encode(self, data):
        """Encodes the data in Base64."""
        return base64.b64encode(data).decode('utf-8')

    def _base64_decode(self, data):
        """Decodes Base64 encoded data."""
        return base64.b64decode(data)

    def _aes_encrypt(self, data):
        """Encrypts data using AES-256 in CBC mode."""
        cipher = AES.new(self.key, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
        return iv, encrypted_data_base64

    def _aes_decrypt(self, encrypted_data_base64, iv_base64):
        """Decrypts data using AES-256 in CBC mode."""
        iv = base64.b64decode(iv_base64)
        encrypted_data = base64.b64decode(encrypted_data_base64)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode('utf-8')


# Example Usage
encryptor = Encryptor()
password = "my_secure_password"

# Encrypt the password
enc_data = encryptor.encrypt(password)

# Decrypt the password
iv, encrypted_password, key = enc_data
decrypt_result = encryptor.decrypt(iv, encrypted_password)
