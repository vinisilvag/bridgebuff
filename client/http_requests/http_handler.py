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
        addr_info = socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        
        # Tentar se conectar preferencialmente usando IPv6
        cliente_socket = None
        for addr in addr_info:
            family, socktype, proto, canonname, sockaddr = addr
            try:
                cliente_socket = socket.socket(family, socktype, proto)
                cliente_socket.settimeout(self.timeout)  # Definir tempo limite
                cliente_socket.connect(sockaddr)
                break  # Conexão bem-sucedida, sair do loop
            except (socket.timeout, socket.error):
                if cliente_socket:
                    cliente_socket.close()
                cliente_socket = None
        
        if cliente_socket is None:
            raise Exception("Não foi possível conectar ao servidor usando IPv4 ou IPv6")
        
        try:
            # Formular a requisição
            linha_requisicao = f"{method} {path} HTTP/1.1\r\n"
            cabecalhos  = f"Host: {self.host}\r\nConnection: keep-alive\r\n\r\n"
            requisicao = linha_requisicao + cabecalhos
            print("\n---------REQUISIÇÃO---------\n" + requisicao)

            # Enviar a requisição
            cliente_socket.sendall(requisicao.encode('utf-8'))
            
            # Receber a resposta
            resposta = b""
            while True:
                # Usar select para aguardar dados para leitura
                ready_to_read, _, _ = select.select([cliente_socket], [], [], self.timeout)
                
                if ready_to_read:
                    parte = cliente_socket.recv(4096)
                    if not parte:
                        break
                    resposta += parte
                else:
                    raise socket.timeout("Tempo limite de leitura excedido")
            
            cliente_socket.close()
            
            if resposta:
                # Split the response into headers and body
                header_body_split = resposta.split(b'\r\n\r\n', 1)
                if len(header_body_split) == 2:
                    header = header_body_split[0]
                    body = header_body_split[1]
                    return (header.decode('utf-8'), body.decode('utf-8'))

                else:
                    print("Invalid HTTP response format")
                    return resposta.decode('utf-8')
            
        except socket.timeout:
            raise Exception("Tempo limite de comunicação com o servidor excedido.")
        except socket.error:
            print("Falha no estabelecimento de conexão com o servidor.")
            raise

