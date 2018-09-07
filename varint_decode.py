#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实现varint 和 zigzag 编码转换器
varint编解码 对于一个整形数字，一般使用 4 个字节来表示一个整数值， varint就是保留每个字节的最高位的 bit 来标识是否后面还有字节，\
1 表示还有字节需要继续读，0 表示到读到当前字节就结束。
zigzag 将负数编码成正奇数，正数编码成偶数。解码的时候遇到偶数直接除 2 就是原值，遇到奇数就加 1 除 2 再取负就是原值。
"""


class Varint(object):

    def __init__(self, num):
        self.num = num

    @classmethod
    def _zigzag_decode(cls, num):
        retval = num * 2 if num > 0 else -2 * num - 1
        return retval

    @classmethod
    def _zigzag_encode(cls, num):
        retval = num / 2 if not num % 2 else -(num + 1) / 2
        return retval

    @classmethod
    def int_to_var(cls, num):
        num = cls._zigzag_encode(num)
        front = rear = count = 0
        while True:
            if num >> 7:
                temp = num & 0x7f
                if rear:
                    rear += (temp | 0x80) << 8
                else:
                    rear = temp
                count += 1
                num >>= 7
            else:
                front = num
                break
            if count:
                front = (front | 0x80) << count * 8
            return front + rear

    @classmethod
    def var_to_int(cls, num):
        front = rear = count = 0
        while True:
            if num >> 8:
                temp = num & 0x7f
                if rear:
                    rear |= temp << 7
                else:
                    rear = temp
                count += 1
                num >>= 8
            else:
                front = num & 0x7f
                break
        if count:
            front <<= count * 7
        return cls._zigzag_decode(front + rear)


