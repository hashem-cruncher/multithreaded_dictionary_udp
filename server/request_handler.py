#!/usr/bin/env python3
"""
Request Handler Module

This module implements the worker pool architecture for processing UDP dictionary requests.
"""

import threading
import json
import logging
import socket
import time

# Configure logging
logger = logging.getLogger('RequestHandler')

class RequestHandlerPool:
    """
    A pool of worker threads that process dictionary lookup requests.
    """
    
    def __init__(self, dictionary, request_queue, num_handlers=5):
        """
        Initialize the request handler pool.
        
        Args:
            dictionary: The dictionary manager
            request_queue: Queue of incoming requests to process
            num_handlers (int): Number of handler threads to create
        """
        self.dictionary = dictionary
        self.request_queue = request_queue
        self.num_handlers = num_handlers
        self.handlers = []
        self.running = False
        self.response_socket = None
        
        # Create UDP socket for sending responses
        try:
            self.response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as e:
            logger.error(f"Error creating response socket: {e}")
            raise
            
    def start(self):
        """
        Start the request handler pool.
        """
        logger.info(f"Starting request handler pool with {self.num_handlers} handlers")
        self.running = True
        
        # Create and start handler threads
        for i in range(self.num_handlers):
            handler = threading.Thread(
                target=self._handler_thread,
                args=(i,),
                name=f"Handler-{i}"
            )
            handler.daemon = True
            handler.start()
            self.handlers.append(handler)
            
        logger.info("Request handler pool started")
        
    def stop(self):
        """
        Stop the request handler pool.
        """
        logger.info("Stopping request handler pool")
        self.running = False
        
        # Wait for handlers to finish (with timeout)
        for handler in self.handlers:
            handler.join(timeout=2.0)
            
        # Close response socket
        if self.response_socket:
            try:
                self.response_socket.close()
                logger.info("Closed response socket")
            except socket.error as e:
                logger.error(f"Error closing response socket: {e}")
                
        logger.info("Request handler pool stopped")
        
    def _handler_thread(self, handler_id):
        """
        Handler thread function that processes requests from the queue.
        
        Args:
            handler_id (int): The handler thread ID
        """
        logger.info(f"Handler {handler_id} started")
        
        while self.running:
            try:
                # Get a request from the queue with timeout
                try:
                    data, client_address, timestamp = self.request_queue.get(timeout=0.5)
                except:
                    continue
                    
                # Calculate time in queue
                queue_time = time.time() - timestamp
                if queue_time > 1.0:
                    logger.warning(f"Request from {client_address} spent {queue_time:.2f}s in queue")
                
                # Process the request
                logger.debug(f"Handler {handler_id} processing request from {client_address}")
                self._process_request(data, client_address, handler_id)
                
                # Mark task as complete
                self.request_queue.task_done()
                
            except Exception as e:
                logger.error(f"Handler {handler_id} error: {e}")
                
        logger.info(f"Handler {handler_id} stopped")
        
    def _process_request(self, data, client_address, handler_id):
        """
        Process a request and send a response.
        
        Args:
            data (bytes): The request data
            client_address (tuple): The client address (host, port)
            handler_id (int): The handler thread ID
        """
        try:
            # Decode JSON request
            try:
                request = json.loads(data.decode('utf-8'))
                action = request.get('action')
                word = request.get('word', '')
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from {client_address}")
                self._send_error_response(client_address, "Invalid JSON format")
                return
            except UnicodeDecodeError:
                logger.warning(f"Invalid encoding from {client_address}")
                self._send_error_response(client_address, "Invalid encoding")
                return
                
            # Process based on action
            if action == 'lookup':
                if not word:
                    self._send_error_response(client_address, "Missing word parameter")
                    return
                    
                # Look up the word
                definition = self.dictionary.lookup(word)
                
                # Send response
                if definition:
                    self._send_response(client_address, {
                        'status': 'found',
                        'word': word,
                        'definition': definition
                    })
                else:
                    self._send_response(client_address, {
                        'status': 'not_found',
                        'word': word
                    })
            else:
                logger.warning(f"Unknown action '{action}' from {client_address}")
                self._send_error_response(client_address, f"Unknown action: {action}")
                
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            self._send_error_response(client_address, "Internal server error")
            
    def _send_response(self, client_address, response_data):
        """
        Send a JSON response to the client.
        
        Args:
            client_address (tuple): The client address (host, port)
            response_data (dict): The response data to send
        """
        try:
            # Add timestamp to response
            response_data['timestamp'] = time.time()
            
            # Encode response as JSON
            response_json = json.dumps(response_data)
            
            # Send the response
            self.response_socket.sendto(response_json.encode('utf-8'), client_address)
            logger.debug(f"Sent response to {client_address}")
            
        except socket.error as e:
            logger.error(f"Error sending response to {client_address}: {e}")
        except Exception as e:
            logger.error(f"Error preparing response: {e}")
            
    def _send_error_response(self, client_address, error_message):
        """
        Send an error response to the client.
        
        Args:
            client_address (tuple): The client address (host, port)
            error_message (str): The error message
        """
        self._send_response(client_address, {
            'status': 'error',
            'message': error_message
        })