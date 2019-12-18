"""
httpserver 2.0
"""
from socket import *
from select import select

class HTTPServer:
    def __init__(self,host='0.0.0.0',port=80,dir=None):
        self.host = host
        self.port = port
        self.address = (host,port)
        self.dir = dir
        self.rlist = []
        self.wlist = []
        self.xlist = []
        # 直接创建套接字
        self.create_socket()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,
                               SO_REUSEADDR,
                               1)
        self.sockfd.bind(self.address)

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d"%self.port)
        # IO多路服用方法监控IO
        self.rlist.append(self.sockfd)
        while True:
            rs,ws,xs=select(self.rlist,
                            self.wlist,
                            self.xlist)
            for r in rs:
                if r is self.sockfd:
                    # 浏览器链接
                    c,addr = r.accept()
                    self.rlist.append(c)
                else:
                    # 处理具体请求
                    self.handle(r)

    # 处理客户端请求
    def handle(self,connfd):
        request = connfd.recv(4096).decode()
        print(request)



if __name__ == '__main__':
    # 通过HTTPServer类快速搭建服务
    # 通过该服务让浏览器访问到我的网页
    # 1. 使用流程
    # 2. 需要用户确定的内容

    # 用户决定的参数
    HOST = '0.0.0.0'
    PORT = 8000
    DIR = './static'
    httpd = HTTPServer(HOST,PORT,DIR) # 生成对象
    httpd.serve_forever() # 启动服务