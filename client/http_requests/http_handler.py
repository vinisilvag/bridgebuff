import json
import socket


class HttpClientHandler:
    def __init__(self, host, port=5000, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout

    def make_get_request(self, path):
        return self._make_request("GET", path)

    def make_head_request(self, path):
        return self._make_request("HEAD", path)

    def _host_resolve(self):
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

        return client_socket

    def _make_request(self, method, path):
        client_socket = self._host_resolve()

        try:
            # Formular a requisição
            request_line = f"{method} {path} HTTP/1.1\r\n"

            headers = {
                "Host": self.host,
                "Content-Type": "application/json",
                "Connection": "keep-alive",
            }
            header_line = ""
            for key, value in headers.items():
                header_line += f"{key}: {value}\r\n"

            request = request_line + header_line + "\r\n"

            # print("---------REQUISIÇÃO---------\n" + request)

            # Enviar a requisição
            client_socket.sendall(request.encode("utf-8"))

            # Receber a resposta
            response = b""
            header_data = b""
            while True:
                content = client_socket.recv(1)
                if not content:
                    break

                header_data += content

                # Check if headers are complete
                if b"\r\n\r\n" in header_data:
                    break

            headers = header_data.decode("utf-8")

            # Obter o tamanho do corpo a ser recebido por meio do cabecalho "content-length"
            header_lines = headers.split("\r\n")
            content_length = None
            for line in header_lines:
                if line.lower().startswith("content-length:"):
                    content_length = int(line.split(":")[1].strip())
                    break

            # ler o corpo da resposta de acordo com o tamanho
            if content_length is not None:
                remaining_length = content_length
                while remaining_length > 0:
                    content = client_socket.recv(1)
                    if not content:
                        break
                    response += content
                    remaining_length -= 1

            # Fechar o socket
            client_socket.close()

            # Decodificar e retornar a resposta
            if response:
                try:
                    response_json = json.loads(response.decode("utf-8"))
                    return response_json
                except json.JSONDecodeError:
                    raise Exception("Falha ao decodificar a resposta como um JSON")

        except socket.timeout:
            raise Exception("Tempo limite de comunicação com o servidor excedido.")
        except socket.error:
            raise Exception("Falha no estabelecimento de conexão com o servidor.")
