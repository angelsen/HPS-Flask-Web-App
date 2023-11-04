import os
import binascii

# Generate a key
key = binascii.hexlify(os.urandom(24)).decode()
print(key)