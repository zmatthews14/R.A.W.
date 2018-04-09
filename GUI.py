import wx
import pyodbc
import datetime
import os

class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(size=(800, 675), *args, **kwargs)

        self.SetBackgroundColour('RED')

        self.Centre()
        self.panel = wx.Panel(self)

        self.png = wx.Image('Logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.logo = wx.StaticBitmap(self.panel, -1, self.png, pos=(75, 10), size=(self.png.GetWidth(), self.png.GetHeight()))
        self.TextBox = wx.StaticText(self.panel, -1, 'Enter Username: ', pos=(270, 530))
        self.Font = self.TextBox.GetFont().Larger().Bold()
        self.TextBox.SetFont(self.Font)

        self.Username = wx.TextCtrl(self.panel, pos=(390, 531), size=(100, 20))

        self.button = wx.Button(self.panel, -1, 'Enter', pos=(355, 555), size=(60, 20))
        self.Font4 = self.button.GetFont().Bold()
        self.button.SetFont(self.Font4)
        self.button.Bind(wx.EVT_BUTTON, self.OnClick)

        self.result = wx.StaticText(self.panel, -1, pos=(340, 580))
        self.Font2 = self.result.GetFont().Larger().Bold()
        self.result.SetFont(self.Font2)
        self.result2 = wx.StaticText(self.panel, -1, pos=(230, 580))
        self.Font3 = self.result2.GetFont().Larger().Bold()
        self.result2.SetFont(self.Font3)


        self.SetTitle('RAW Match Login')
        self.Show(True)

    def OnClick(self,e):
        username = self.Username.GetValue()
        open('Matches.txt', 'w').close()

        conn = pyodbc.connect('Driver={SQL Server}; '
                              'Server=rawdatabase.cak10k15cn9o.us-east-2.rds.amazonaws.com; '
                              'Database=RAW; '
                              'uid=LH;pwd=Lighthouse#12')

        day = str(datetime.date.today().day)
        today = datetime.date.today().strftime('%A, %B ' + day + ', %Y')

        currentTime = datetime.datetime.now()
        hour = currentTime.hour
        minute = currentTime.minute

        if len(str(minute)) == 1:
            newMinute = '0' + str(minute)
        else:
            newMinute = str(minute)

        if hour > 12:
            hour = hour - 12
            time = str(hour) + ':' + str(newMinute) + ' PM'
        else:
            if hour == 12:
                time = str(hour) + ':' + str(newMinute) + ' PM'
            elif hour == 0:
                hour = 12
                time = str(hour) + ':' + str(newMinute) + ' AM'
            else:
                time = str(hour) + ':' + str(newMinute) + ' AM'

        cursor = conn.cursor()
        SQLCommand = "SELECT MatchID, Matchmaker, Opponent, Time, Result FROM dbo.Matches WHERE UserArmID = ? AND Day = ?"
        Values = ['UPub - Amherst, MA', today]
        cursor.execute(SQLCommand, Values)
        results = cursor.fetchone()

        # add todays matches to text file
        while results:
            if results[4] is None:
                file = open('Matches.txt', 'a')
                file.write(str(results[0]) + ' ' + str(results[1]) + ' ' + str(results[2]) + ' ' + str(results[3]))
                file.close()
            results = cursor.fetchone()

        cursor = conn.cursor()
        SQLCommand = "SELECT Matchmaker, Opponent, Time, Result FROM dbo.Matches WHERE OpponentArm = ? AND Day = ?"
        Values = ['UPub - Amherst, MA', today]
        cursor.execute(SQLCommand, Values)
        results = cursor.fetchone()

        while results:
            if results[4] is None:
                file = open('Matches.txt', 'a')
                file.write(str(results[0]) + ' ' + str(results[2]) + ' ' + str(results[1]) + ' ' + str(results[3]))
                file.close()
            results = cursor.fetchone()

        lineCounter = 0
        file = open('Matches.txt', 'r')

        if os.stat('Matches.txt').st_size == 0:
            self.result2.SetLabel('There are currently no matches on this arm')
        else:
            for line in file:
                matchParts = line.split(' ')
                if matchParts[1] == username:
                    timeEnd = time.split(' ')
                    matchParts3DropEnd = matchParts[4].split('\n')
                    if matchParts3DropEnd[0] == timeEnd[1]:
                        splitMatchHM = matchParts[3].split(':')
                        splitHM = timeEnd[0].split(':')
                        if splitMatchHM[0] == 12:
                            splitMatchHM[0] = 0
                        if splitHM[0] == 12:
                            splitHM[0] = 0

                        if splitMatchHM[0] == splitHM[0]:
                            minuteDiff = int(splitMatchHM[1]) - int(splitHM[1])
                            if minuteDiff <= 2 and minuteDiff >= -2:
                                self.result.SetLabel('You may begin match')
                                file2 = open('ActiveMatch.txt', 'w')
                                file2.write(matchParts[0] + ' ' + matchParts[1] + ' ' + matchParts[2] + ' start')
                                file2.close()
                            elif minuteDiff > 2:
                                self.result.SetLabel('You are too early')
                            elif minuteDiff < -2:
                                self.result.SetLabel('You are too late')
                        elif splitMatchHM[0] > splitHM[0]:
                            self.result.SetLabel('You are too early')
                        elif splitMatchHM[0] < splitHM[0]:
                            self.result.SetLabel('You are too late')
                    elif matchParts3DropEnd[0] == 'PM' and timeEnd == 'AM':
                        self.result.SetLabel('You are too early')
                    elif matchParts3DropEnd[0] == 'AM' and timeEnd == 'PM':
                        self.result.SetLabel('You are too late')
                else:
                    self.result.SetLabel('No match found')

                lineCounter = lineCounter + 1

        file.close()
        conn.close()

def main():
    app = wx.App()
    windowClass(None)
    app.MainLoop()

main()
