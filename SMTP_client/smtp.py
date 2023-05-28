import base64
import json
import mimetypes
import os
import socket
import ssl
from datetime import time

HOST_ADDR = 'smtp.yandex.ru'
PORT = 465
BUFFER_LEN = 1024

attachments_path = None
user_name_from = None
arr_user_name_to = None
subject_msg = None


def request(sock, request):
    sock.send((request + '\n').encode())
    sock.setblocking(0)  # Устанавливаем неблокирующий режим работы сокета
    recv_data = b""
    while True:
        try:
            chunk = sock.recv(BUFFER_LEN)
            if not chunk:
                break
            recv_data += chunk
        except socket.error as e:
            if e.errno == socket.errno.EWOULDBLOCK:  # Нет доступных данных для получения
                time.sleep(1)
                continue
            else:
                break
    return recv_data.decode("UTF-8")


def message_prepare():
    with open('msg.txt', 'r', encoding='UTF-8') as file_msg:
        boundary_msg = "bound.40629"
        headers = f'from: {user_name_from}\n'
        headers += f'to: {arr_user_name_to}\n'  # пока получатель один
        headers += f'subject: {subject_msg}\n'  # короткая тема на латинице
        headers += 'MIME-Version: 1.0\n'
        headers += 'Content-Type: multipart/mixed;\n' \
                   f'    boundary={boundary_msg}\n'

        # тело сообщения началось
        msg = file_msg.read()
        message_body = f'--{boundary_msg}\n' \
                       'Content-Type: text/plain; charset=utf-8\n\n' \
                       f'{msg}\n'

        for filename in os.listdir(attachments_path):
            mime_type = mimetypes.guess_type(filename)

            with open(attachments_path + '/' + filename, 'rb') as attachment:
                str_attachment = base64.b64encode(attachment.read()).decode()

            message_body += f'--{boundary_msg}\n' \
                            'Content-Disposition: attachment;\n' \
                            f'\tfilename="{filename}"\n' \
                            'Content-Transfer-Encoding: base64\n' \
                            f'Content-Type: {mime_type[0]};\n' \
                            f'\tname="{filename}"\n\n' \
                            f'{str_attachment}\n'

        message_body += f'--{boundary_msg}--'

        message = headers + '\n' + message_body + '\n.\n'
        print(message)
        return message


def main():
    global arr_user_name_to, attachments_path, subject_msg, user_name_from
    with open('config.json', 'r', encoding='UTF-8') as json_file:  # новое
        file = json.load(json_file)
        user_name_from = file['from']  # считываем из конфига кто отправляет
        arr_user_name_to = file['to']  # считываем из конфига кому отправляем (сделать список)
        subject_msg = file['subject']
        attachments_path = file['attachments_path']

    with open("pswd.txt", "r", encoding="UTF-8") as file:
        password = file.read().strip()  # считываем пароль из файла

    ssl_contex = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_contex.check_hostname = False
    ssl_contex.verify_mode = ssl.CERT_NONE

    with socket.create_connection((HOST_ADDR, PORT)) as sock:
        with ssl_contex.wrap_socket(sock, server_hostname=HOST_ADDR) as client:
            print(client.recv(1024))  # в smpt сервер первый говорит
            print(request(client, f'ehlo {user_name_from}'))
            base64login = base64.b64encode(user_name_from.encode()).decode()

            base64password = base64.b64encode(password.encode()).decode()
            print(request(client, 'AUTH LOGIN'))
            print(request(client, base64login))
            print(request(client, base64password))
            print(request(client, f'MAIL FROM:{user_name_from}'))
            for user_name_to in arr_user_name_to:
                print(request(client, f"RCPT TO:{user_name_to}"))
            print(request(client, 'DATA'))
            print(request(client, message_prepare()))
            print(request(client, 'QUIT'))


if __name__ == '__main__':
    main()
