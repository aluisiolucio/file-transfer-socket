import os
import socket
import time
from hashlib import md5


def conect_to_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    return sock

def send_file_data(sock, client_id, file_path):
    try:
        if not os.path.isfile(file_path):
            print("O arquivo não existe. Por favor, insira um nome de arquivo válido.")
            return
        
        sock.send(client_id.encode())
        time.sleep(2)

        file_name = file_path.split('/')[-1]
        sock.send(file_name.encode())
        time.sleep(5)

        with open(file_path, "rb") as file:
            data = file.read(1024)
            while data:
                sock.send(data)
                data = file.read(1024)

        print(f"Arquivo {file_path} enviado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao enviar o arquivo: {str(e)}")

def client_socket(client_name, filename):
    host = "127.0.0.1"
    port = 5556

    sock = conect_to_server(host, port)

    # while True:
    #     filename = input("Insira o nome do arquivo que você deseja enviar (ou 'exit' para sair): ")
        
    #     if filename.lower() == 'exit':
    #         break
    client_id = md5(client_name.encode()).hexdigest()
    
    try:
        send_file_data(sock, client_id, filename)
    finally:
        sock.close()

if __name__ == "__main__":
    try:
        client_socket("aluisio123", "/home/aluisio/github/file-transfer-socket/file.txt")
    except KeyboardInterrupt:
        print("\nPrograma finalizado pelo usuário.")
