import socket

ADDR = ("", 12349)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

