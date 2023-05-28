import json
import ntplib
import socket


def main():
    with open("config.json", "r") as file_json:
        file = json.load(file_json)
        seconds = file['seconds']

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 123))

    print("Server is starting...")
    print(f"Time deviation: {seconds} seconds.")

    while True:
        data, addr = udp_socket.recvfrom(1024)

        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('time.windows.com', version=3)
        ntp_time = response.tx_time

        modified_time = ntp_time + seconds
        time_bytes = str(modified_time).encode()
        udp_socket.sendto(time_bytes, addr)


if __name__ == '__main__':
    main()
