import socketimport 
import yaml
# Function to send encrypted data via TCP and receive the response
def load_config(file='config.yaml'):
    """
    Load the configuration from a YAML file.
    This config file should contain the expected error message from the server.
    """
    with open(file, 'r') as f:
        return yaml.safe_load(f)
def send_tcp_data(host, port, data):
    """
    Sends encrypted data via a TCP connection and returns the server's response.
    Data is expected in hexadecimal format.
    """
    config = load_config()
    print(f"Connecting to {host} on port {port}")
    try:
        # Create the TCP socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Sending data: {data}")
            # Send the data (convert from hex to bytes)
            s.sendall(bytes.fromhex(data))
            # Receive the server's response (1024 byte buffer)
            response = s.recv(1024)
            if response==config["error_mesage"]:
            	return False
            else:
            	return True
    except Exception as e:
        print(f"Error during TCP connection: {e}")
        return None
