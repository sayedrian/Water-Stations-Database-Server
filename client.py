import socket
import time

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 54321
WAITING_TIME = 0.1

def validate_parameters(lines):
    """
    Check if water station parameters are valid.
    """
    if all(item.isdigit() for item in lines) and int(lines[1]) in [0, 1] and int(lines[2]) in [0, 1]:
        return True
    else:
        print('')
        print('ERROR: Please check the file parameters and try again.')
        print('First line is the station ID, must be a number. It cannot be empty.')
        print('Second and third lines represent the state of Alarms 1 & 2 (0 for OFF; 1 for ON).')
        return False

def validate_file(filename):
    """
    Check if the file exists and its content is valid.
    """
    try:
        with open(filename, 'r') as f:
            station_status = f.read().splitlines()
            message = '-'.join(str(i) for i in station_status)
            if validate_parameters(station_status):
                return message
            else:
                return None
    except FileNotFoundError:
        print('ERROR: File not found. Please check the file name, extension, and path.')
        return None

if __name__ == '__main__':
    try:
        with socket.socket() as s:
            server_address = (SERVER_ADDRESS, SERVER_PORT)
            try:
                s.connect(server_address)
            except socket.error:
                print('')
                print("SOCKET ERROR: Client couldn't make connection. Please check if the server is available.")
                print('')
                print('Before uploading the data, make sure the server is available.')

            while True:
                file_name = input("Please enter the water station status file name or 'q' to quit: ")
                if file_name.lower() == 'q':
                    print('Connection shutdown. Goodbye!')
                    break

                file_data = validate_file(file_name)
                if file_data is not None:
                    try:
                        s.send(file_data.encode())
                        response = s.recv(1024).decode()
                        print("---> ", response)
                        print()
                        time.sleep(WAITING_TIME)
                    except socket.error as er:
                        print('')
                        print("Socket error occurred. Please check the connection before you try again.")
                        print('')
                        break
                else:
                    print('File is corrupted. Please try again or quit.')
                    continue

    except KeyboardInterrupt:
        pass
    finally:
        print()
        print("Closing client socket.")
        s.close()
        print("Goodbye!")
