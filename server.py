import socket
import threading
import queue
import time

def create_server_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def bind_and_listen(sock, host, port, total_clients):
    sock.bind((host, port))
    sock.listen(total_clients)

def handle_client(connection):
    file_extension = connection.recv(1024).decode()

    timestamp = str(time.time()).replace('.', '')
    filename = f"received_file_{timestamp}{file_extension}"

    try:
        with open(filename, "wb") as file:
            data = connection.recv(1024)
            while data:
                file.write(data)
                data = connection.recv(1024)

        print(f"Arquivo {filename} recebido com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao receber o arquivo: {str(e)}")

    finally:
        connection.close()
        print("Conexão fechada.")

def main():
    host = "0.0.0.0"
    port = 5556
    total_clients = 5  # Defina o número desejado de clientes simultâneos

    sock = create_server_socket()
    bind_and_listen(sock, host, port, total_clients)

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

