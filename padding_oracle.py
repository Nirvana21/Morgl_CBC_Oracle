import argparse
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

# 2. Main function to handle the Padding Oracle attack
def padding_oracle_attack(host, port, encrypted_data):
    """
    Main function for the Padding Oracle attack.
    It sends data over TCP and waits for the server's response.
    """
    print(f"Connecting to {host}:{port}")

    # Send the encrypted data and receive the server's response
    response = send_tcp_data(host, port, encrypted_data)
    
    print(f"Server response: {response.hex()}")
    # Logic for the attack can be added here

if __name__ == "__main__":
    # 3. Retrieve arguments and start the attack
    args = parse_args()
    padding_oracle_attack(args.host, args.port, args.data)
