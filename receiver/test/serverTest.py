# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

import socket
import struct
import testEncode


HOST = 'localhost'
PORT = 6690



def main():
    try:
        s = socket.socket()

        rbsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print " send buf is ", rbsize

        s.bind(('0.0.0.0', PORT))
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
    main()







