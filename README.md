# UDP Dictionary Server

A multithreaded dictionary server and client implementation using UDP sockets, JSON data format, and worker pool architecture.

## 📋 Project Overview

This project implements a client-server dictionary application that allows users to look up word definitions. Key features include:

- **UDP Communication**: Uses connectionless protocol for fast, lightweight communication
- **Worker Pool Architecture**: Efficiently handles multiple concurrent client requests
- **JSON Data Format**: Stores dictionary entries in a structured, extensible format
- **Multithreading**: Manages concurrent operations with thread synchronization
- **PyQt5 GUI**: Provides a responsive graphical interface for the client

## 🏗️ Project Structure

```
multithreaded_dictionary_udp/
├── server/
│   ├── __init__.py           # Empty file to make directory a package
│   ├── udp_server.py         # Main UDP server implementation
│   ├── request_handler.py    # Worker pool implementation
│   └── json_dictionary.py    # Dictionary manager for JSON data
│
├── client/
│   ├── __init__.py           # Empty file to make directory a package
│   ├── udp_client_gui.py     # PyQt5 GUI client application
│   └── udp_client_comm.py    # UDP client communication module
│
├── data/
│   ├── __init__.py           # Empty file to make directory a package
│   └── dictionary.json       # Dictionary data in JSON format
│
├── README.md                 # This documentation file
└── requirements.txt          # Project dependencies (PyQt5)
```

## ✨ Features

- **Fast Communication**: UDP protocol for low-overhead networking
- **Concurrent Processing**: Multiple worker threads process client requests
- **Rich Dictionary Data**: Includes definitions, categories, and synonyms
- **Responsive GUI**: Modern interface with search functionality
- **Client-Side Caching**: Improves performance for repeated lookups
- **Comprehensive Error Handling**: Handles network failures with retry mechanism
- **Thread Synchronization**: Prevents race conditions during concurrent operations

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/udp-dictionary-server.git
cd udp-dictionary-server
```

2. Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🖥️ Running the Application

### Starting the Server

```bash
# From the project root
cd server
python udp_server.py 8888 ../data/dictionary.json
```

**Command-line arguments:**
- `8888`: UDP port to listen on
- `../data/dictionary.json`: Path to the dictionary file

### Starting the Client

```bash
# From the project root
cd client
python udp_client_gui.py localhost 8888
```

**Command-line arguments:**
- `localhost`: Server address
- `8888`: Server UDP port

## 🧪 Testing the Application

### Basic Testing

1. Start the server
2. Launch the client
3. Enter a word (e.g., "algorithm") in the search box
4. Click "Search" or press Enter
5. Verify that the definition appears in the result area

### Multiple Clients Testing

1. Start the server
2. Launch multiple client instances from different terminals
3. Perform lookups from different clients simultaneously
4. Verify that all clients receive correct responses

### Error Handling Testing

1. **Server Not Running**: 
   - Start client without starting server
   - Verify appropriate error message and retry attempts

2. **Unknown Word**:
   - Look up a non-existent word
   - Verify that a "Not found" message is displayed

3. **Server Restart**:
   - Start server and client
   - Shut down and restart the server
   - Try lookups after restart
   - Verify client recovers connection

## 📊 Protocol Details

### UDP Communication

Unlike TCP, UDP doesn't establish a connection before sending data. This project implements reliability at the application level:

- **Request IDs**: Each request gets a unique identifier
- **Timeouts**: Client waits for responses with timeout
- **Retries**: Automatically retries failed requests
- **JSON Encoding**: Data is formatted as JSON for both requests and responses

### Request Format

```json
{
  "action": "lookup",
  "word": "algorithm",
  "timestamp": 1713493200.123,
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Response Format

```json
{
  "status": "found",
  "word": "algorithm",
  "definition": "A step-by-step procedure for solving a problem...",
  "timestamp": 1713493200.456
}
```

## 🔧 Worker Pool Architecture

The server implements a worker pool architecture:

1. Main thread: Listens for incoming UDP packets
2. Request queue: Holds client requests
3. Worker threads: Process requests from the queue
4. Thread synchronization: Prevents race conditions

This design efficiently handles multiple concurrent clients while controlling resource usage.

## 📔 Dictionary Format

The dictionary is stored in JSON format with the following structure:

```json
{
  "metadata": {
    "title": "Technology Dictionary",
    "description": "A dictionary of technology terms",
    "version": "1.0"
  },
  "entries": [
    {
      "word": "algorithm",
      "definition": "A step-by-step procedure for solving a problem",
      "category": "computing",
      "synonyms": ["procedure", "process"]
    }
  ]
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **"Address already in use" Error**:
   - Wait a few minutes for the port to be released
   - Use a different port: `python udp_server.py 8889 ../data/dictionary.json`

2. **PyQt5 Installation Issues**:
   - Windows: `pip install --upgrade pip` followed by `pip install PyQt5`
   - Linux: `sudo apt-get install python3-pyqt5`
   - macOS: `brew install pyqt5`

3. **No Response from Server**:
   - Check that server is running
   - Verify that firewall is not blocking UDP traffic
   - Ensure correct server address and port

## 🚀 Extending the Project

### Adding Words

To add words to the dictionary:

1. Open `data/dictionary.json`
2. Add new entries to the "entries" array following the existing format
3. Save the file and restart the server

### Feature Ideas

- Add search by category
- Implement word suggestions
- Create a server administration interface
- Add user accounts and custom dictionaries
- Implement performance monitoring and statistics

