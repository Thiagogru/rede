import socket
import os


def send_file(filename, server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    BUFFER_SIZE = 500  # Tamanho menor de pacote

    try:
        # Enviar o nome do arquivo primeiro
        file_name = os.path.basename(filename)
        # Adicionar uma nova linha para separar o nome do arquivo
        file_name = f"{file_name}\n".encode()
        client_socket.sendto(file_name, (server_ip, server_port))
        print(f"Nome do arquivo '{file_name.decode().strip()}' enviado.")

        with open(filename, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                client_socket.sendto(data, (server_ip, server_port))
                print(f"Enviado {len(data)} bytes.")  # Log de depuração

        # Enviar uma mensagem de término
        client_socket.sendto(b'END_OF_FILE\n', (server_ip, server_port))
        print("Mensagem de término enviada.")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
    except IOError as e:
        print(f"Erro de I/O: {e}")
    finally:
        client_socket.close()
        print("Arquivo enviado com sucesso.")


if __name__ == "__main__":
    # Inclua a extensão do arquivo
    FILE_TO_SEND = "C:/Users/gruen/Pictures/compiladores/CompiladoresLista1-1.jpg"
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 12345
    send_file(FILE_TO_SEND, SERVER_IP, SERVER_PORT)
