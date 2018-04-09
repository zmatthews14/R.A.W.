import pyodbc
import os

conn = pyodbc.connect('Driver={SQL Server}; '
                            'Server=rawdatabase.cak10k15cn9o.us-east-2.rds.amazonaws.com; '
                            'Database=RAW; '
                            'uid=LH;pwd=Lighthouse#12')

updateResultFile = open('FinishedMatch.txt', 'r')
for line in updateResultFile:
    finishedMatchParts = line.split(' ')
    matchID = finishedMatchParts[0]
    result = finishedMatchParts[1]

    cursor = conn.cursor()
    SQLCommand = "UPDATE dbo.Matches SET Result = ? WHERE MatchID = ?"
    Values = [result, matchID]
    cursor.execute(SQLCommand, Values)
    conn.commit()

updateResultFile.close()
os.remove('FinishedMatch.txt')
conn.close()
