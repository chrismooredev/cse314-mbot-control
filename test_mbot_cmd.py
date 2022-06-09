
import sys
import time
import mbot

m=mbot.MBot()

m.send(sys.argv[1] + '\n')
time.sleep(1) # give time for bot to respond
print(m.read())

