import os
import socket
from dotenv import load_dotenv
from hashlib import md5

load_dotenv()


def conect_to_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    return sock

def send_file_data(sock, filename):
    try:
        # Verifica se o arquivo existe
        if not os.path.isfile(filename):
            print("O arquivo não existe. Por favor, insira um nome de arquivo válido.")
            return

        # Envia o nome do arquivo (incluindo a extensão)
        file_extension = os.path.splitext(filename)[1]
        sock.send(file_extension.encode())

        # Abre o arquivo e envia os dados
        with open(filename, "rb") as file:
            data = file.read(1024)
            while data:
                sock.send(data)
                data = file.read(1024)

        print(f"Arquivo {filename} enviado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao enviar o arquivo: {str(e)}")

def client_socket():
    host = "127.0.0.1"
    port = 5556

    sock = conect_to_server(host, port)

    while True:
        filename = input("Insira o nome do arquivo que você deseja enviar (ou 'exit' para sair): ")
        
        if filename.lower() == 'exit':
            break

        send_file_data(sock, filename)

    sock.close()

if __name__ == "__main__":
    try:
        client_socket()
    except KeyboardInterrupt:
        print("\nPrograma finalizado pelo usuário.")
