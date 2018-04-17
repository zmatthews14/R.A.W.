import wx
import datetime
import xmlrpclib

s = xmlrpclib.ServerProxy('http://:8080/', allow_none=True)

class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(size=(800, 675), *args, **kwargs)

        self.Centre()
        self.panel = wx.Panel(self)

        self.png = wx.Image('Logo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.logo = wx.StaticBitmap(self.panel, -1, self.png,pos=(50, 0), size=(700, 480))
        self.TextBox = wx.StaticText(self.panel, -1, 'Enter Username: ', pos=(270, 485))
        self.Font = self.TextBox.GetFont().Larger().Bold()
        self.TextBox.SetFont(self.Font)

        self.Username = wx.TextCtrl(self.panel, pos=(420, 487), size=(100, 20))

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

    def OnClick(self,e):
        username = self.Username.GetValue()

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

        if s.Find_Matches() == 'No matches':
            self.result2.SetLabel('There are currently no matches on this arm')
        else:
            matchData = s.Find_Matches().split(' ')
            file = open('Matches.txt', 'a')
            file.write(matchData[0] + ' ' + matchData[1] + ' ' + matchData[2] + ' ' + matchData[3])

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

def main():
    app = wx.App()
    windowClass(None)
    app.MainLoop()

main()
