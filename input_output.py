import socket

def send_tcp_data(s, data):
    """
    Sends encrypted data via an existing TCP connection and returns the server's response.
    """
    try:
        s.sendall(data.encode())  # Send data as bytes
        response = s.recv(4096).decode()  # Receive and decode the server's response
        response = response.strip()

        
        if "Error" in response:
            return False  # Padding error detected
        return True  # Valid padding
    except (socket.gaierror, TimeoutError) as e:
        print(f"Network error: {e}. Skipping this byte...")
        return False
