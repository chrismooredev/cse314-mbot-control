#!/usr/bin/python3

import sys
import socket

emac = '00:1B:10:60:4C:9E' # external bluetooth module MAC addr
port = 3 # not sure

class MBot(object):
    def __init__(self, on_dist=None):
        self.s = socket.socket(socket.AF_BLUETOOTH, proto=socket.BTPROTO_RFCOMM)
        print('connecting...')
        self.s.connect((emac, port))
        self.s.setblocking(False)
        print('connected')
        
        self.sendlines = []
        self.recvbuf = bytearray()
        self.recvlines = []

        self.on_dist = None

    def reconnect(self):
        if self.s is not None: self.s.close()

        self.s = socket.socket(socket.AF_BLUETOOTH, proto=socket.BTPROTO_RFCOMM)
        print('connecting...', file=sys.stderr)
        self.s.connect((emac, port))
        # self.s.setblocking(False)
        print('connected', file=sys.stderr)

    def move(self,left_deg, right_deg, left_speed = 100, right_speed = 100):
        self.send(f"Move,{left_deg},{right_deg},{left_speed},{right_speed}\n")

    def query_dist_cm(self):
        self.send("QueryDistanceCM\n")
    
    def send(self, msg):
        # add msg to send buffer
        self.sendlines.append(msg)

        try:
            while len(self.sendlines) > 0:
                # we have some buffered messages, try to send them first
                head = self.sendlines[0]
                self.s.send(bytes(head, "UTF-8"))
                _ = self.sendlines.pop(0)
        except BlockingIOError as e:
            print("Error sending messages. In queue: " + int(len(self.sendlines)), file=sys.stderr)
    
    def read(self):
        msgbuf = []
        try:
            self.recvbuf += self.s.recv(2048)
            nl = self.recvbuf.find(b"\n")
            while nl != -1:
                msgb = self.recvbuf[:nl]
                msgs = msgb.decode('UTF-8', errors='replace')
                if msgs.startswith('!'):
                    msgbuf.append(msgs[1:].split(','))
                else:
                    print('[rover] ' + msgs)
                self.recvbuf = self.recvbuf[nl+1:]
                nl = self.recvbuf.find(b"\n")
        except BlockingIOError as e:
            pass
        return msgbuf
