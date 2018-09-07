#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""简单的套接字 server端"""
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8080))
sock.listen(1)
while True:
    conn, addr = sock.accept()  # 接收一个客户端连接
    print(conn.recv(1024))      # 从接收缓冲读消息 recv buffer
    conn.send("world")          # 将响应发送到发送缓冲 send buffer
    conn.close()                # 关闭连接

# agent端
sock_agent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_agent.connect(("localhost", 8080))   # 连接服务器
sock_agent.sendall("hello")               # 将消息输出到发送缓冲 send buffer
print(sock_agent.recv(1024))              # 从接收缓冲recv buffer中读响应
sock_agent.close()                        # 关闭套接字

