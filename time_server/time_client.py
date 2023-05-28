import socket
from datetime import datetime


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 123)

    # Отправка запроса на получение времени
    udp_socket.sendto(b"TimeRequest", server_address)

    # Получение ответа от сервера
    data, server = udp_socket.recvfrom(1024)
    print("Received a response from the server:")
    time_value = float(data.decode())

    formatted_datetime = datetime.fromtimestamp(time_value).strftime("%d.%m.%y %H:%M:%S")
    print("Date and Time:", formatted_datetime)

    udp_socket.close()


if __name__ == '__main__':
    main()