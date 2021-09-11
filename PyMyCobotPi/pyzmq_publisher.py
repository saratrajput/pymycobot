import zmq
import random
import sys
import time

port = "8000"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

my_string = "Hello"

while True:
    print("Sending message")
    message = input("Enter string to send: ")
    socket.send_string(message)
    # socket.send_string(my_string)
    time.sleep(1)