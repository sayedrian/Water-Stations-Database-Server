import socket
import sqlite3 as sq
from datetime import datetime

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 54321
DATABASE_PATH = 'data.sqlite'

class Client:
    def __init__(self, socket=None, ip=None, port=None):
        self.socket = socket
        self.ip = ip
        self.port = port

def create_connection():
    conn = None
    try:
        conn = sq.connect(DATABASE_PATH)
    except sq.Error as e:
        print("Error connecting to the database:", e)
    return conn

def create_db(conn):
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS station_status (
                           station_id INTEGER,
                           date_time TEXT,
                           alarm1 INTEGER,
                           alarm2 INTEGER,
                           PRIMARY KEY (station_id)
                           )""")
    except sq.Error as e:
        print("Error creating database table:", e)

def update_db(conn, st_id, a1, a2):
    try:
        with conn:
            cur = conn.cursor()
            date_time = str(datetime.now())
            cur.execute("INSERT OR REPLACE INTO station_status VALUES (?, ?, ?, ?)",
                        (st_id, date_time, a1, a2))
    except sq.Error as e:
        print("Error updating database:", e)

def main():
    try:
        conn = create_connection()
        if conn is None:
            return

        create_db(conn)

        print("Starting server at", datetime.now().strftime('%Y-%M-%d %H:%m'))
        server_address = (SERVER_ADDRESS, SERVER_PORT)
        with socket.socket() as s:
            s.bind(server_address)
            s.listen(10)
            s.settimeout(0.001)

            client_list = []
            print("\nListening on IP:", SERVER_ADDRESS, "Port:", SERVER_PORT)

            while True:
                try:
                    c = s.accept()
                    client = Client(socket=c[0], ip=c[1][0], port=c[1][1])
                    client.socket.settimeout(0.001)
                    client_list.append(client)
                    print("New client connected from:", client.ip, "Port:", client.port)
                except socket.error:
                    pass

                for client in list(client_list):
                    try:
                        message = client.socket.recv(1024).decode()
                        if not message:
                            client_list.remove(client)
                            print("Client disconnected:", client.ip, "Port:", client.port)
                            continue
                        status = message.split('-')
                        update_db(conn, status[0], status[1], status[2])
                        client.socket.send(b"Water station is updated")
                    except socket.error:
                        pass

    except KeyboardInterrupt:
        pass
    finally:
        if conn:
            conn.close()
        print("\nClosing server socket")
        print("Goodbye!")

if __name__ == "__main__":
    main()
