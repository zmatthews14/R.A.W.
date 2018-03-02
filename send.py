import socket
import serial
import time

#UDP_IP = "128.119.82.231"
UDP_IP = "169.254.68.246"
#UDP_PORT = 5005
UDP_PORT = 4800

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser = serial.Serial('/dev/ttyS0',9600)

while True:
    try:
        if(ser.inWaiting()>0):
            arduinoPWM = ser.readline()
            print arduinoPWM
            sock.sendto(arduinoPWM,(UDP_IP,UDP_PORT))
    except socket.error, e:
        print"socket error ", e
        sock.close()
        break
