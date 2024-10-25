import argparse
from input_output import send_tcp_data
import os
import socket

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

# 2. Main function to handle the Padding Oracle attack
def padding_oracle_attack(host, port, encrypted_data):
    """
    Main function for the Padding Oracle attack.
    It sends data over TCP and waits for the server's response.
    """
    encrypted_data = bytearray.fromhex(encrypted_data)  # Convert hexadecimal string to bytearray
    resp = []
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        while len(encrypted_data) > 16:
            print("ON VA S'OCCUPER DES BLOCS")
            encrypted_data_final = encrypted_data[-16:]
            encrypted_data = encrypted_data[:-16]
            random_block = bytearray(os.urandom(16))

            for i in range(1, 17):
                tmp_random = bytearray(random_block)  # Copy random_block to tmp_random
                for j in range(1, i):
                    tmp_random[-j] = i ^ resp[j - 1] ^ encrypted_data[-j]
                
                for moving_byte in range(256):
                    tmp_random[-i] = moving_byte
                    payload = tmp_random + encrypted_data_final

                    # Send the encrypted data and receive the server's response
                    response = send_tcp_data(s, payload.hex())
                    if response:
                        print("on ajoute le bit")
                        resp.append(moving_byte ^ encrypted_data[-i] ^ i)
                        break
                else:
                    print(f"On a rien trouvé pour le byte {i}")
    
    print("La réponse est")
    for number in reversed(resp):
        print(hex(number))


if __name__ == "__main__":
    # 3. Retrieve arguments and start the attack
    args = parse_args()
    padding_oracle_attack(args.host, args.port, args.data)
