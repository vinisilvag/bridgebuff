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
            except socket.error:
                if cliente_socket:
                    cliente_socket.close()
                cliente_socket = None
        
        if cliente_socket is None:
            raise Exception("Não foi possível conectar ao servidor usando IPv4 ou IPv6")
        
        try:
            # Formular a requisição
            linha_requisicao = f"{method} {path} HTTP/1.1\r\n"
            cabecalhos =  ""#f"Host: {self.host}" #\r\nConnection: close\r\n\r\n"
            requisicao = linha_requisicao + cabecalhos
            
            # Enviar a requisição
            cliente_socket.sendall(requisicao.encode('utf-8'))
            
            # Receber a resposta
            resposta = b""
            while True:
                # Usar select para aguardar dados para leitura
                print(requisicao)
                ready_to_read, _, _ = select.select([cliente_socket], [], [], self.timeout)
                
                if ready_to_read:
                    parte = cliente_socket.recv(4096)
                    if not parte:
                        break
                    resposta += parte
                    print(json.loads(parte.decode('utf-8')) )
                    print(parte.hex())
                else:
                    raise socket.timeout("Tempo limite de leitura excedido")
        
        except socket.timeout:
            raise Exception("Tempo limite excedido durante a comunicação com o servidor")
        
        finally:
            # Fechar o socket
            cliente_socket.close()
        
        # Decodificar e retornar a resposta
        return resposta.decode('utf-8')

