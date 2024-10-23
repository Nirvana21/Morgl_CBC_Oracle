# Utility function to convert bytes to a readable hexadecimal format
def bytes_to_hex(data):
    return data.hex()

# Function to convert hexadecimal data to bytes
def hex_to_bytes(hex_data):
    return bytes.fromhex(hex_data)
