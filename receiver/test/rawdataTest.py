# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

import socket
import struct
import testEncode


HOST = 'localhost'
PORT = 6688


def testSyncQuery(s):
    ins = testEncode.syncQuery()
    data = ins.groupNetData()
    print "syncQuery Frame on network is:"
    print repr(data)
    print "send sync data to server"
    s.sendall(data)
    data = s.recv(1024)
    print('received', repr(data))

def testWashStep(s):
    devId = 0x09010009;
    month = 3
    for i in range(1,20):
        ins = testEncode.WashStep(month, i, devId+i%3, i%8)
        data = ins.groupNetData()
        print "WashStep frame on network is:"
        print repr(data)
        print "send WashStep data to server"
        s.sendall(data)
        data = s.recv(1024)
        print('received', repr(data))

def testRptPumpCfg(s):
    ins = testEncode.RptPumpCfg()
    data = ins.groupNetData()
    print "RptPumpCfg frame on network is:"
    print repr(data)
    print "send RptPumpCfg data to server"
    s.sendall(data)
    data = s.recv(1024)
    print('received', repr(data))    


def main():
    """
    with open('rawdata', 'rb') as f:
        buf = f.read()
    print len(buf)
    data = buf[386:-4]
    with open('tmp', 'wb') as f2:
        f2.write(data)
    """
    with open('tmp', 'rb') as f:
        data = f.read()
    print len(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))   
    s.sendall(data)
    data = s.recv(1024)
    print('received', repr(data))  
    #testSyncQuery(s)
    #testWashStep(s)
    #testRptPumpCfg(s)
    #s.close()

"""
while True:
    msg = syncData
    s.sendall(msg)

    data = s.recv(1024)
    print('received', repr(data))
"""
    




if __name__ == '__main__':
    main()







