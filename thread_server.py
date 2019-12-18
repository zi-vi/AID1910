"""
thread_server.py 基于Thread线程并非
重点代码

创建监听套接字
循环接收客户端连接请求
当有新的客户端连接创建线程处理客户端请求
主线程继续等待其他客户端连接
当客户端退出，则对应分支线程退出
"""
from socket import *
from threading import Thread
import os

ADDR = ('0.0.0.0',8888)

# 客户端处理函数,循环收发消息
def handle(c):
    while True:
        data = c.recv(1024).decode()
        if not data:
            break
        print(data)
        c.send(b'OK')

# 创建监听套接字
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

print("Listen the port 8888....")

while True:
    # 循环等待客户端连接
    try:
        c,addr = s.accept()
        print("Connect from",addr)
    except KeyboardInterrupt:
        os._exit(0)
    except Exception as e:
        print(e)
        continue

    # 创建新的线程处理请求
    client = Thread(target=handle,args=(c,))
    client.setDaemon(True)
    client.start()


