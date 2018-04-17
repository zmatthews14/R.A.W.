#import matplotlib
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import time

fileLine = 0

while(True):
    print 'wait for start'
    numbersList = np.zeros(15,)
    while not os.path.exists('Start.txt'):
        time.sleep(1)
    os.remove('Start.txt')
            
    file = open('ForceNumbers.txt','r')
    line = file.seek(fileLine)
    while(line != 'end\n'):
        if(line == 'end\n'):
            
            #plt.close()
            #plt.gcf()
            print line
            break
        if(line == '\n'):
            pass
        else:
            lineInt = int(line)
            numbersSplit = np.split(numbersList, [1])
            numbersList = np.append(numbersSplit[1], [lineInt])
            strainGaugeCurrent = numbersList / 12.234
            torque = strainGaugeCurrent * 16.2298228
            force = torque / .235
            print force
            print numbersList
            plt.clf()
            plt.plot(numbersList)
            plt.ylim((0,50))
            plt.ylabel('Torque (N*m)')
            plt.draw()
            plt.pause(.001)
        if fileLine = 20:
            fileLine = 0
        else:
            fileLine = fileLine + 1
        line = file.seek(fileLine)
    file.close()
