import hashlib
import base64

def hash_and_encode(input_string):
    # Create a sha256 hash object
    sha256_hash = hashlib.sha256()
    
    # Update the hash object with the string encoded to bytes
    sha256_hash.update(input_string.encode('utf-8'))
    
    # Get the hashed string in hexadecimal format
    hashed_string = sha256_hash.digest()  # .digest() returns the raw bytes
    print(hashed_string)
    
    # Encode the hashed bytes into base32
    base32_encoded = base64.b32encode(hashed_string).decode('utf-8')
    
    return base32_encoded

# Example usage
input_string = "HelloWorld"
encoded_string = hash_and_encode(input_string)
print(f"Original String: {input_string}")
print(f"Base32 Encoded String: {encoded_string}")
