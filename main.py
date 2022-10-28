import socket
from server_multiple import MyTCPHandler
import socketserver
import threading
from threadstest import myThread

l = [(423424, 0, "sfsfs"),
     (234224, 5, "qdasqfas"),
     (42342342, 10, "fqfafqwfa")]
for i in range(len(l) - 1):
    if l[i][0] == 423424:
        pos = i
        l.pop(pos)

print(l)
