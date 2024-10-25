import unittest
from unittest.mock import MagicMock, patch
import random
import socket
from padding_oracle import create_random_block, modify_block_for_padding, send_tcp_data

class TestPaddingOracle(unittest.TestCase):

    def test_create_random_block(self):
        """Test that the random block generated has the correct size."""
        block_size = 16
        random_block = create_random_block(block_size)
        self.assertEqual(len(random_block), block_size)
        # Ensure the block contains bytes (0-255)
        for byte in random_block:
            self.assertTrue(0 <= byte <= 255)

    def test_modify_block_for_padding(self):
        """Test that the block is modified correctly for padding."""
        block = bytearray([random.randint(0, 255) for _ in range(16)])
        byte_position = 5  # Modify the 5th byte from the end
        value = 0xFF
        padding_size = 5

        modified_block = modify_block_for_padding(block, byte_position, value, padding_size)

        # Check that the correct byte has been modified
        expected_value = block[-byte_position] ^ padding_size ^ value
        self.assertEqual(modified_block[-byte_position], expected_value)

        # Ensure bytes already modified by padding are correctly adjusted
        for i in range(1, byte_position):
            expected_value = block[-i] ^ padding_size ^ (padding_size + 1)
            self.assertEqual(modified_block[-i], expected_value)

    @patch('socket.socket')
    def test_send_tcp_data(self, mock_socket):
        """Test that data is sent correctly over TCP and responses are received."""
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.return_value = b"OK\n"
        
        # Create a mock socket object
        mock_socket_instance.sendall = MagicMock()

        # Call the function
        response = send_tcp_data(mock_socket_instance, 'test_data')

        # Ensure sendall was called with the correct data
        mock_socket_instance.sendall.assert_called_with(b'test_data')
        # Test if the function correctly interprets the response
        self.assertTrue(response)

    @patch('socket.socket')
    def test_send_tcp_data_with_padding_error(self, mock_socket):
        """Test when padding error is detected in the response."""
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.return_value = b"System.Security.Cryptography.CryptographicException: Padding Error\n"
        
        # Create a mock socket object
        mock_socket_instance.sendall = MagicMock()

        # Call the function
        response = send_tcp_data(mock_socket_instance, 'test_data')

        # Ensure sendall was called with the correct data
        mock_socket_instance.sendall.assert_called_with(b'test_data')
        # Test if the function detects the padding error
        self.assertFalse(response)

if __name__ == '__main__':
    unittest.main()
