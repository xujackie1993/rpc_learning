#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import struct
import socket
import thread


def loop(sock, handlers):
    while True:
        conn, addr = sock.accept()  # 接收连接
        thread.start_new_thread(handle_conn, (conn, addr, handlers))  # 开启一个新的线程来处理连接


def handle_conn(conn, addr, handlers):
    print(addr, "comes")
    while True:
        length_prefix = conn.recv(4)   # 请求长度前缀
        if not length_prefix:
            print(addr, "bye")
            conn.close()
            break     # 退出循环，处理下一个连接
        length, = struct.unpack("I", length_prefix)
        print(length)
        body = conn.recv(length)
        request = json.loads(body)
        in_ = request["in"]
        params = request["params"]
        print(in_, params)
        handler = handlers[in_]
        handler(conn, params)


def ping(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result})
    length_prefix = struct.pack("I", len(response))
    print(type(length_prefix))
    conn.sendall(length_prefix)
    conn.sendall(response)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 创建一个tcp套接字
    # 选项value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，
    # 否则操作系统会保留几分钟该端口。
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 打开 reuse addr
    sock.bind(("localhost", 8080))  # 绑定端口
    sock.listen(1)     # 监听客户端
    handlers = {        # 注册请求处理器
        "ping": ping
    }
    loop(sock, handlers)  # 进入服务循环
