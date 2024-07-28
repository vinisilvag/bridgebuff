import socket
import json
import select


class HttpClientHandler:
    def __init__(self, host, port=5000, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout

    def make_get_request(self, path):
        return self._make_request("GET", path)

    def make_head_request(self, path):
        return self._make_request("HEAD", path)

    def _make_request(self, method, path):
        # Resolver o host para obter informações de endereço
        addr_info = socket.getaddrinfo(
            self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM
        )

        # Tentar se conectar preferencialmente usando IPv6
        client_socket = None
        for addr in addr_info:
            family, socktype, proto, _, sockaddr = addr
            try:
                client_socket = socket.socket(family, socktype, proto)
                client_socket.settimeout(self.timeout)  # Definir tempo limite
                client_socket.connect(sockaddr)
                break  # Conexão bem-sucedida, sair do loop
            except (socket.timeout, socket.error):
                if client_socket:
                    client_socket.close()
                client_socket = None

        if client_socket is None:
            raise Exception("Não foi possível conectar ao servidor usando IPv4 ou IPv6")

        try:
            # Formular a requisição
            linha_requisicao = f"{method} {path} HTTP/1.1\r\n"
            cabecalhos = f"Host: {self.host}\r\nConnection: keep-alive\r\n\r\n"
            requisicao = linha_requisicao + cabecalhos
            print("---------REQUISIÇÃO---------\n" + requisicao)

            # Enviar a requisição
            client_socket.sendall(requisicao.encode("utf-8"))

            # Receber a resposta
            response = b""
            header_data = b""
            while True:
                # Usar select para aguardar dados para leitura
                ready_to_read, _, _ = select.select(
                    [client_socket], [], [], self.timeout
                )

                if ready_to_read:
                    part = client_socket.recv(4096)
                    if not part:
                        break
                    header_data += part
                    # Check if headers are complete
                    if b"\r\n\r\n" in header_data:
                        break
                else:
                    raise socket.timeout("Tempo limite de leitura excedido")

            # Separa os dados de cabecalho e corpo
            headers, body = header_data.split(b"\r\n\r\n", 1)
            headers = headers.decode("utf-8")
            response += body

            # Obter o tamanho do corpo a ser recebido por meio do cabecalho "content-length"
            header_lines = headers.split("\r\n")
            content_length = None
            for line in header_lines:
                if line.lower().startswith("content-length:"):
                    content_length = int(line.split(":")[1].strip())
                    break

            # ler o corpo da resposta de acordo com o tamanho
            if content_length is not None:
                remaining_length = content_length - len(body)
                while remaining_length > 0:
                    part = client_socket.recv(min(4096, remaining_length))
                    if not part:
                        break
                    response += part
                    remaining_length -= len(part)

            # Fechar o socket
            client_socket.close()

            # Decodificar e retornar a resposta
            if response:
                try:
                    response_json = json.loads(response.decode("utf-8"))
                    return response_json
                except json.JSONDecodeError:
                    print("Failed to decode response as JSON")
                    return response.decode("utf-8")

        except socket.timeout:
            raise Exception("Tempo limite de comunicação com o servidor excedido.")
        except socket.error:
            print("Falha no estabelecimento de conexão com o servidor.")
            raise
