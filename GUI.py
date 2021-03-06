import wx
import datetime
import xmlrpclib
import os
import time as TIME

s = xmlrpclib.ServerProxy('http://localhost:8000', allow_none=True)

class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(size=(800, 675), *args, **kwargs)

        self.Centre()
        self.panel = wx.Panel(self)

        self.png = wx.Image('Logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.logo = wx.StaticBitmap(self.panel, -1, self.png, pos=(50, 0), size=(700, 480))

        self.TextBox = wx.StaticText(self.panel, -1, 'Enter Username: ', pos=(270, 485))
        self.Font = self.TextBox.GetFont().Larger().Bold()
        self.TextBox.SetFont(self.Font)

        self.Username = wx.TextCtrl(self.panel, pos=(420, 487), size=(100, 20))
        self.Username.Bind(wx.EVT_TEXT, self.OnTouch)

        self.button = wx.Button(self.panel, -1, 'Enter', pos=(355, 515), size=(60, 30))
        self.Font4 = self.button.GetFont().Bold()
        self.button.SetFont(self.Font4)
        self.button.Bind(wx.EVT_BUTTON, self.OnClick)

        self.result = wx.StaticText(self.panel, -1, pos=(340, 555))
        self.Font2 = self.result.GetFont().Larger().Bold()
        self.result.SetFont(self.Font2)
        self.result2 = wx.StaticText(self.panel, -1, pos=(230, 555))
        self.Font3 = self.result2.GetFont().Larger().Bold()
        self.result2.SetFont(self.Font3)

        self.SetTitle('RAW Match Login')
        self.Show(True)

    def OnTouch(self, e):
        self.result.SetLabel("")
        self.result2.SetLabel("")

    def OnClick(self,e):
        username = self.Username.GetValue()
        open('Matches.txt','w').close()

        lateRange = 0
        earlyRange = 0
        matchTimeInMinutes = 0

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

        timeArray = time.split(' ')
        timeHourMinute = timeArray[0].split(':')
        AMPM = timeArray[1]
        Hour = timeHourMinute[0]
        Minutes = timeHourMinute[1]

        hourToMinutes = int(Hour) * 60
        currentTimeInMinutes = 0

        if AMPM == 'PM':
            PMaddOn = 720
            currentTimeInMinutes = PMaddOn + hourToMinutes + int(Minutes)
        else:
            currentTimeInMinutes = hourToMinutes + int(Minutes)


        if s.Find_Matches() == 'No matches':
            self.result2.SetLabel('There are currently no matches on this arm')
        else:
            matchList = s.Find_Matches()
            while len(matchList) != 0:
                grabber = matchList.pop(0)
                matchData = str(grabber).split(' ')
                file = open('Matches.txt', 'a')
                file.write(matchData[0] + ' ' + matchData[1] + ' ' + matchData[2] + ' ' + matchData[3] + ' ' + matchData[4] + '\n')

        file = open('Matches.txt', 'r')
        for line in file:
            matchParts = line.split(' ')
            if matchParts[1] == username:
                matchAMPM = matchParts[4].split('\n')
                matchHourMinute = matchParts[3].split(':')

                matchHourtoMinutes = int(matchHourMinute[0]) * 60

                if matchAMPM[0] == 'PM':
                    PMaddOn = 720
                    matchTimeInMinutes = PMaddOn + matchHourtoMinutes + int(matchHourMinute[1])
                else:
                    matchTimeInMinutes = matchHourtoMinutes + int(matchHourMinute[1])

                earlyRange = matchTimeInMinutes - currentTimeInMinutes
                lateRange = currentTimeInMinutes - matchTimeInMinutes

                if earlyRange <= 30 and lateRange <= 30:
                    self.result.SetLabel('You may begin match')
                    file2 = open('ActiveMatch.txt', 'w')
                    file2.write(matchParts[0] + ' ' + matchParts[1] + ' ' + matchParts[2] + ' start')
                    file2.close()
                    while os.path.exists('FinishedMatch.txt') is False:
                        self.result.SetLabel('You may begin match')
                        TIME.sleep(2)
                    updateResultFile = open('FinishedMatch.txt', 'r')
                    for line in updateResultFile:
                        finishedMatchParts = line.split(' ')
                        matchID = finishedMatchParts[0]
                        result = finishedMatchParts[1]
                        if username == result:
                            self.result.SetLabel('YOU WON!!!!')
                        else:
                            self.result.SetLabel('You Lost :( ')
                        print s.Update_Match_Results(result, matchID)
                    updateResultFile.close()
                    os.remove('FinishedMatch.txt')
                elif earlyRange > 30 and lateRange < -30:
                    self.result.SetLabel('You are too early')
                elif lateRange > 30 and earlyRange < -30:
                    self.result.SetLabel('You are too late, Match Expired')
                    updateResultFile = open('FinishedMatch.txt', 'w')
                    updateResultFile.write(matchParts[0] + ' Expired')
                    updateResultFile.close()
                    updateResultFile = open('FinishedMatch.txt', 'r')
                    for line in updateResultFile:
                        finishedMatchParts = line.split(' ')
                        matchID = finishedMatchParts[0]
                        result = finishedMatchParts[1]
                        print s.Update_Match_Results(result, matchID)
                    updateResultFile.close()
                    os.remove('FinishedMatch.txt')
            else:
                self.result.SetLabel('No match found')

def main():
    app = wx.App()
    windowClass(None)
    app.MainLoop()

main()
