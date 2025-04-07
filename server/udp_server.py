#!/usr/bin/env python3
"""
UDP Dictionary Server

This module implements a multithreaded dictionary server using UDP sockets.
It loads dictionary data from a JSON file and responds to client requests.
"""
import sys
import os
import socket
import threading
import logging
import signal
import time
import json
import queue
from server.request_handler import RequestHandlerPool
from server.json_dictionary import DictionaryManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s [%(name)s] - %(message)s"
)
logger = logging.getLogger("UDPDictionaryServer")

# Initialize server variable for use in signal handler
server = None


class UDPDictionaryServer:
    """
    UDP Dictionary Server that handles client requests using a pool of worker threads.
    """

    def __init__(self, port, dictionary_file, num_handlers=5, buffer_size=1024):
        """
        Initialize the UDP Dictionary Server.

        Args:
            port (int): UDP port to listen on
            dictionary_file (str): Path to the JSON dictionary file
            num_handlers (int): Number of request handler threads
            buffer_size (int): Size of the UDP packet buffer
        """
        self.port = port
        self.dictionary_file = dictionary_file
        self.num_handlers = num_handlers
        self.buffer_size = buffer_size
        self.socket = None
        self.request_queue = queue.Queue()
        self.running = False

        # Initialize dictionary
        try:
            self.dictionary = DictionaryManager(dictionary_file)
            logger.info(f"Loaded dictionary with {self.dictionary.count()} entries")
        except Exception as e:
            logger.error(f"Failed to load dictionary: {e}")
            raise

        # Initialize request handler pool
        self.handler_pool = RequestHandlerPool(
            self.dictionary, self.request_queue, num_handlers
        )

    def start(self):
        """
        Start the UDP dictionary server.
        """
        # Create UDP socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(("", self.port))
            self.socket.settimeout(0.5)  # Short timeout to allow for clean shutdown
            logger.info(f"Server started on UDP port {self.port}")
        except socket.error as e:
            logger.error(f"Socket error: {e}")
            raise

        # Start request handler pool
        self.handler_pool.start()
        self.running = True

        # Start receive loop
        self._receive_loop()

    def _receive_loop(self):
        """
        Main loop to receive UDP packets and queue them for processing.
        """
        try:
            while self.running:
                try:
                    # Receive data from client
                    data, client_address = self.socket.recvfrom(self.buffer_size)

                    # Queue the request for processing
                    logger.debug(f"Received request from {client_address}")
                    self.request_queue.put((data, client_address, time.time()))

                except socket.timeout:
                    # Expected due to socket timeout
                    continue
                except socket.error as e:
                    if not self.running:
                        break
                    logger.error(f"Socket error: {e}")

        except KeyboardInterrupt:
            logger.info("Server interrupted by user")
        finally:
            self.stop()

    def stop(self):
        """
        Stop the server and clean up resources.
        """
        logger.info("Shutting down server...")
        self.running = False

        # Stop request handler pool
        if hasattr(self, "handler_pool"):
            self.handler_pool.stop()

        # Close socket
        if self.socket:
            try:
                self.socket.close()
                logger.info("Closed UDP socket")
            except socket.error as e:
                logger.error(f"Error closing socket: {e}")

        logger.info("Server shutdown complete")


def signal_handler(sig, frame):
    """Handle signals for clean shutdown."""
    logger.info(f"Received signal {sig}, shutting down...")
    if "server" in globals() and server is not None:
        server.stop()
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python udp_server.py <port> <dictionary-file>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        dictionary_file = sys.argv[2]

        # Validate arguments
        if port < 1024 or port > 65535:
            print("Error: Port must be between 1024 and 65535")
            sys.exit(1)

        if not os.path.exists(dictionary_file):
            print(f"Error: Dictionary file '{dictionary_file}' not found")
            sys.exit(1)

        # Start server
        server = UDPDictionaryServer(port, dictionary_file)
        server.start()

    except ValueError:
        print("Error: Port must be a number")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        logger.error(f"Error starting server: {e}", exc_info=True)
        sys.exit(1)
