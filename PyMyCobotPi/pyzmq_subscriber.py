import sys
import zmq

port = "8000"

# Socket to talk to server
context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.setsockopt(zmq.SUBSCRIBE, b"")
print("Subscriber connecting...")
sub.connect("tcp://192.168.0.108:{}".format(port))

while True:
    print("Receiving")
    my_string = sub.recv_string()
    print(my_string)