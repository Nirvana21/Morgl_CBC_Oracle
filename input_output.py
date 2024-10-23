import socket
import yaml

# Function to load the configuration file
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
    Data is expected in hexadecimal string format.
    """
    config = load_config()
    print(f"Connecting to {host} on port {port}")
    
    try:
        # Create the TCP socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            s.sendall(data.encode())  # Send the data as a string, encoded to bytes
            
            # Receive the server's response (increase buffer size if necessary)
            response = s.recv(4096).decode()  # Decode the byte response to string

            
            # Strip the response to remove trailing whitespace and newlines
            response = response.strip()

            
            # Compare the decoded response with the error message from the config
            if config['error_message'] in response:

                return False
            else:

                return True

    except socket.gaierror as e:

        return False  # Return False to signal that the padding wasn't valid due to connection failure

