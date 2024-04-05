# Water Stations Database Server (Python, SQLite, Socket Communication)

In this project, I developed a database server to efficiently manage water stations' data. Multiple client stations can communicate with this server, ensuring smooth data transmission and storage. Leveraging Python, SQLite, and socket communication, the system effectively monitors and updates water station information in the SQL database, providing a streamlined solution for tracking water management data.

## Project Structure

The project consists of the following files:

- `server.py`: Represents the server.
- `data.sqlite`: SQLite 3 database used by the server to store client data. It resides in the same directory as the server.
- `client.py`: Represents a single client. This file is meant to be copied to different folders and executed for each station.
- `status.txt`: Contains the data of the client. Each `status.txt` file should be copied to the same folder as `client.py`, with different data inside (at least a different ID).

## Client Implementation

The client runs in a loop, reading data from its respective `status.txt`, connecting to the server, and sending the data. It repeats this process every 60 seconds. Ensure the client closes `status.txt` after reading to allow for manual changes.

The `status.txt` file structure:
1. First line: Station ID (integer)
2. Second line: State of Alarm1 (0 for OFF; 1 for ON)
3. Third line: State of Alarm2 (0 for OFF; 1 for ON)

Example `status.txt` content:
```
123
0
1
```

## Server Implementation

Upon initialization, the server opens `data.sqlite` (creating it if it doesn't exist) and creates a table for station data if not already present. The server then enters a loop to receive client data and update the database accordingly.

The database table `station_status` contains the following columns:
- `station_id`: Primary key for station ID
- `last_date`: Date of the last contact with the server (formatted as "YYYY-MM-DD HH:mm")
- `alarm1`: State of Alarm1 (0 or 1)
- `alarm2`: State of Alarm2 (0 or 1)

If a received station ID doesn't exist in the database, a new line is inserted. If the station ID exists, its fields are updated.

## Important Notes

- Ensure the server is SQL-injection safe.
- The server socket binds to IP 127.0.0.1 for testing purposes.
- Exception handling should be implemented in the server code.
- The server should handle incoming data from multiple clients simultaneously.

## Usage

To run the project:
1. Copy `client.py` and `status.txt` to different folders for each station.
2. Update `status.txt` for each station with appropriate data.
3. Execute `client.py` in each station folder.
4. Run `server.py` to start the server.

**Note:** Data exchange between clients and the server occurs using sockets, with data sent as encoded strings separated by spaces.

For further details, refer to the project's source code.
