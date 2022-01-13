import socket
from typing import Tuple
URLS={
    '/':"Hello world!",
    '/blog':"Hello, this is blog"
}

def parse_request(request:str)->Tuple[str, str]:
    """Парсит ответ на тип запроса и url"""
    print(request)
    parsed = request.split(' ')
    method=parsed[0]
    url=parsed[1]
    return (method,url)

def generate_headers(method:str,url:str)-> Tuple[str, int]:
    """Генерирует заголовки страницы"""
    if method!='GET':
        return ('HTTP/1.1 405 Method not allowed\n\n',405)
    if  url not in URLS:
        return ('HTTP/1.1 404 Not found\n\n',404)

    return ('HTTP/1.1 200 ok\n\n',200)

def generate_content(code:int,url:str)->str:
    """Генерирует контент - страницы"""
    if code == 404:
        return "<h1>404</h1><p>Not found</p>"
    elif code == 405:
        return "<h1>405</h1><p>Method not allowed</p>"
    return f'<h1>{URLS[url]}</h1>'

def generate_response(request:str)->bytes:
    """Генерирует ответ клиента"""
    method,url = parse_request(request)
    print(f'{url}\n')
    headers,code = generate_headers(method,url)
    body = generate_content(code,url)
    return (headers + body).encode()

def run()->None:
    """Запускает приложение на web socket-ах"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_socket.bind(('localhost',5000))
    server_socket.listen()


    # client_socket, addr = server_socket.accept()
    # request = client_socket.recv(1024)
    # print(client_socket.recv(1024))
    # print(request.decode('utf-8'))

    while True:
        client_socket,addr = server_socket.accept() # принимаем клиентский сокет и адрес
        request=client_socket.recv(1024)
        print(request.decode('utf-8'))
        print(type(request))
        response = generate_response(request.decode('utf-8'))
        # print(type(response))
        client_socket.sendall(response)
        client_socket.close()

if __name__ == '__main__':
    run()