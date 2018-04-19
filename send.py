import socket
import serial
import time
import os

#UDP_IP = "128.119.82.231"
UDP_IP = "169.254.68.246"
RECEIVE_IP = "169.254.150.111"
#UDP_PORT = 5005
UDP_PORT = 4800
RECEIVE_PORT = 5000

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser = serial.Serial('/dev/ttyS0',9600)

sock_receive.bind((RECEIVE_IP, RECEIVE_PORT))
sock_receive.setblocking(0)
sock.setblocking(0)

def ensureSend(sendData):
    sentStart = False
    while(sentStart == False):
        try:
            sentStart = True
            sock.sendto(sendData,(UDP_IP,UDP_PORT))
        except socket.error:
            sentStart = False
            pass

gameOver = True
result = ''
addr = ''
oldPWM = 0

while True:
    while(gameOver == True):
        print 'Enter \'start\' to start game'
        ################################
        while os.path.exists('StartMatch.txt') is False:
            time.sleep(2)
        startMatchFile = open('StartMatch.txt','r')
        for line in startMatchFile:
            startParts = line.split(' ')
            matchID = startParts[0]
            armUser = startParts[1]
            opponent = startParts[2]
            input = startParts[3]
            print input
        startMatchFile.close()
        os.remove('StartMatch.txt')
        ################################
        #input = raw_input()
        if(input == 'start'):
            ensureSend(input.encode())
            ser.write('1\r\n')
            open('ForceNumbers.txt','w').close()
            startGraphFile = open('Start.txt','w')
            startGraphFile.close()
            gameOver = False
            break
        print 'Invalid entry'
    try:
        if(ser.inWaiting()>0):
            arduinoPWM = ser.readline()
            print arduinoPWM
            if(oldPWM != arduinoPWM):
                file = open('ForceNumbers.txt','a')
                file.write(arduinoPWM + '\n')
            oldPWM = arduinoPWM
            file.close()
            try:
                sock.sendto(arduinoPWM,(UDP_IP,UDP_PORT))
                #ensureSend(arduinoPWM)
            except socket.error:
                pass
        try:
            result,addr = sock_receive.recvfrom(1024)
        except socket.error:
            result = ''
            addr = ''
            pass
        if(result.decode() == 'win'):
            print 'You Win!'
            ser.write('0\r\n')
            file = open('ForceNumbers.txt','a')
            file.write('end\n')
            file.close()
            ############################
            updateMatchResult = open('FinshedMatch.txt','w')
            updateMatchResult.write(matchID + ' ' + armUser)
            updateMatchResult.close()
            ############################
            #wait for start from user
            gameOver = True
        if(result.decode() == 'lose'):
            print 'You Lose :('
            ser.write('0\r\n')
            file = open('ForceNumbers.txt','a')
            file.write('end\n')
            file.close()
            ############################
            updateMatchResult = open('FinshedMatch.txt','w')
            updateMatchResult.write(matchID + ' ' + opponent)
            updateMatchResult.close()
            #############################
            #wait for start from user
            gameOver = True
    except socket.error, e:
        print"socket error ", e
        sock_receive.close()
        sock.close()
        break