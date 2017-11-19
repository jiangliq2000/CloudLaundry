# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

import sys
import logging
import struct
import socket
import time
import gevent
import traceback
#from gevent import socket, monkey
import lib.encode as encode
import lib.decode as decode
import lib.DbOpt as DbOpt
from lib.const import *

#monkey.patch_all()


BUFFER_LEN = 4096


def server(port):
    try:
        s = socket.socket()

        rbsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print " send buf is ", rbsize

        s.bind(('0.0.0.0', 7000))
        s.listen(100)
  
        while True:
            conn, addr = s.accept()
            print ('--- recive connection from : ' + str(addr))
            client_data = conn.recv(4096)

            print "data len is ", len(client_data)
            conn.sendall("finish")
            conn.close()
 

    except Exception, e:
        print(e)



if __name__ == '__main__':
    server(7000)


