import socket
import threading
import os
import sys


def clear_line():
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()


def receive_messages(receive_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', receive_port))

    while True:
        try:
            message, client_address = server_socket.recvfrom(1024)
            message = message.decode()

            if message.startswith("FILE:"):
                _, file_name = message.split(" ", 1)
                receive_file(file_name, server_socket)
            else:
                clear_line()
                sys.stdout.write(f"Mensagem recebida de {
                                 client_address}: {message}\n")
                sys.stdout.write("Digite a mensagem para enviar ao cliente: ")
                sys.stdout.flush()
        except Exception as e:
            print(f"\nErro ao receber mensagem: {e}")

    server_socket.close()


def send_messages(send_port, target_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            message = input("Digite a mensagem para enviar ao cliente: ")

            if message.startswith("FILE:"):
                _, file_path = message.split(" ", 1)
                send_file(file_path, target_ip, send_port)
            else:
                client_socket.sendto(message.encode(), (target_ip, send_port))

            if message.lower() == 'sair':
                print("Desconectando do servidor.")
                break
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    client_socket.close()


def send_file(file_path, target_ip, send_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if not os.path.isfile(file_path):
        print(f"O arquivo {file_path} não foi encontrado.")
        return

    with open(file_path, "rb") as f:
        file_name = os.path.basename(file_path)
        client_socket.sendto(
            f"FILE:{file_name}".encode(), (target_ip, send_port))
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            client_socket.sendto(chunk, (target_ip, send_port))
        client_socket.sendto(b"EOF", (target_ip, send_port))

    print(f"Arquivo {file_path} enviado com sucesso.")
    client_socket.close()


def receive_file(file_name, server_socket):
    save_path = input("Digite o caminho onde o arquivo deve ser salvo: ")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = os.path.join(save_path, file_name)

    with open(file_path, "wb") as f:
        while True:
            chunk, _ = server_socket.recvfrom(1024)
            if chunk == b"EOF":
                break
            f.write(chunk)

    print(f"Arquivo {file_name} recebido e salvo em {file_path}.")


if __name__ == "__main__":
    receive_port = int(input("Digite a porta para receber mensagens: "))
    send_port = int(input("Digite a porta para enviar mensagens: "))
    target_ip = input(
        "Digite o IP do cliente (ou 'localhost' para mesma máquina): ")

    # Iniciar a thread para receber mensagens
    receive_thread = threading.Thread(
        target=receive_messages, args=(receive_port,))
    receive_thread.daemon = True
    receive_thread.start()

    # Iniciar a thread para enviar mensagens
    send_thread = threading.Thread(
        target=send_messages, args=(send_port, target_ip))
    send_thread.daemon = True
    send_thread.start()

    # Manter o servidor em execução
    receive_thread.join()
    send_thread.join()
