import os
import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8000', allow_none=True)

updateResultFile = open('FinishedMatch.txt', 'r')
for line in updateResultFile:
    finishedMatchParts = line.split(' ')
    matchID = finishedMatchParts[0]
    result = finishedMatchParts[1]
    print s.Update_Match_Results(result, matchID)

updateResultFile.close()
os.remove('FinishedMatch.txt')
