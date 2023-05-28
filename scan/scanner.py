import socket
import multiprocessing as mp
from time import time


def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        try:
            sock.connect((ip, port))
            print(f'TCP PORT : {port} is open.')
            sock.close()
        except:
            pass


def scan_tcp_ports(ip, left, right):
    processes = list()
    for port in range(left, right + 1):
        proc = mp.Process(target=scan_port, args=(ip, port))
        processes.append(proc)
        proc.start()
    for proc in processes:
        proc.join()


def main():
    host = input('Enter host: ')
    left, right = input('Enter left-right borders: ').split('-')
    scan_tcp_ports(host, int(left), int(right))


if __name__ == '__main__':
    main()
