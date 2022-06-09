
import os
import sys
import time
import struct
import socket
import threading
import bluetooth

# specify the BLE MAC to connect with
emac = '00:1B:10:60:4C:9E' # emac
# emac = 'e0:9f:2a:ea:db:a7'
# emac = '00:1B:10:60:4D:9E' # imac
port = 3 # not sure tbh

# setup our connection
# s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# s.setblocking(False)
# s.connect(('00:1B:10:60:4C:9E', 3))

# s = socket.socket(socket.AF_BLUETOOTH, proto=socket.BTPROTO_RFCOMM)
# s.connect(('00:1B:10:60:4C:9E', 3))

def setup_conn():
    global s
    s = socket.socket(socket.AF_BLUETOOTH, proto=socket.BTPROTO_RFCOMM)
    print('connecting...')
    s.connect((emac, port))
    print('connected')

while True:
    try:
        setup_conn()
        def read_loop():
            global s
            buf=bytearray()
            while True:
                try:
                    buf += s.recv(64)
                except TimeoutError as te:
                    setup_conn()
                    continue
                nl = buf.find(b'\n')
                while nl != -1:
                    line = buf[:nl]
                    print(line.decode('utf8', errors='replace'))
                    buf = buf[nl+1:]
                    nl = buf.find(b'\n')

        t=threading.Thread(target=read_loop, name="mbot_log", daemon=True)
        t.start()

        # some initial messages to test with
        # s.send(bytes("msg:Hel\x88lo\n", "UTF-8"))
        s.send(bytes("msg:Hello\n", "UTF-8"))
        s.send(bytes("msg:connected", "UTF-8"))

        # s = socket.socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        # s.connect((emac, port))
        # s.send(bytes('hello!\n', 'UTF-8'))

        
        t.join()

        while True:
            # send a heartbeat on every iteration
            # s.send(bytes("msg:heartbeat\n", "UTF-8"))
            print('.', end='')
            try:
                # ask the user (index.js) for a value
                srssi = int(input('rssi: '))
                # send it to the bot
                s.send(bytes("rssi:%d\n" % srssi, "UTF-8"))
            except Exception as e:
                # don't crash if we didn't receive a numeric value to send
                print("couldn't parse rssi, didn't send", e)

    except Exception as e:
        print("Encounted exception: ", e, file=sys.stderr)
        try:
            print("closing")
            s.close()
        except Exception as _err:
            print("closing exception")
            break
        if isinstance(e, KeyboardInterrupt):
            break
        print("Restarting script...", file=sys.stderr)

