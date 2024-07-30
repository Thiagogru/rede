import socket


def start_server(port, save_dir):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))
    print(f"Servidor escutando na porta {port}")

    # Receber o nome do arquivo
    file_name, _ = server_socket.recvfrom(500)
    file_name = file_name.decode().strip()
    save_path = f"{save_dir}/{file_name}"
    print(f"Nome do arquivo para salvar: {save_path}")

    with open(save_path, 'wb') as f:
        while True:
            data, addr = server_socket.recvfrom(8192)
            if data.endswith(b'END_OF_FILE\n'):
                break
            f.write(data)
            print(f"Recebido {len(data)} bytes.")  # Log de depuração

    print("Arquivo recebido com sucesso.")
    server_socket.close()


if __name__ == "__main__":
    PORT = 12345
    SAVE_DIR = "E:/vsCodeFolder/udptransf1"  # Diretório para salvar o arquivo
    start_server(PORT, SAVE_DIR)
