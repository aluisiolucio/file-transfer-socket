import os
import socket
import threading
import queue
import time


def init_server(host, port, total_clients):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(total_clients)

    return sock

def handle_client(connection):
    client_id = connection.recv(1024).decode()
    print(f"Cliente: {client_id}")
    
    if not os.path.exists(client_id):
        os.mkdir("opt/" + client_id)
    
    file_name = connection.recv(1024).decode()
    print(f"Nome do arquivo: {file_name}")

    timestamp = str(time.time()).replace('.', '')
    file_name = f"{timestamp}_{file_name}"

    try:
        with open(os.path.join("opt", client_id, file_name), "wb") as file:
            data = connection.recv(1024)
            while data:
                file.write(data)
                data = connection.recv(1024)

        print(f"Arquivo {file_name} recebido com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao receber o arquivo: {str(e)}")

    finally:
        connection.close()
        print("Conexão fechada.")

def main():
    host = "0.0.0.0"
    port = 5556
    total_clients = 5

    sock = init_server(host, port, total_clients)

    print(f'Aguardando conexões na porta {port}...')

    active_threads = []
    connection_queue = queue.Queue(maxsize=total_clients)

    try:
        while True:
            try:
                conn, addr = sock.accept()
                print(f'Conexão estabelecida com {addr}')

                if connection_queue.full():
                    print("Limite de clientes atingido. Rejeitando conexão.")
                    conn.close()
                else:
                    connection_queue.put(conn)
                    client_thread = threading.Thread(target=handle_client, args=(conn,), daemon=True)
                    client_thread.start()
                    active_threads.append(client_thread)

            except queue.Full:
                print("A fila de conexões está cheia. Aguardando vaga.")

    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")

    finally:
        for thread in active_threads:
            thread.join()

        sock.close()

if __name__ == "__main__":
    main()

