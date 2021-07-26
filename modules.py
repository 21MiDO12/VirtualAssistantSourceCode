import functions as f
import pTypes as t
import userinterface as ui
import os
import cv2
import threading as th
import time
import datetime as dt


class OnPrelaunch(object):
    """Check everything required for the program to run successfully"""

    def __init__(self):
        if self.checkConfig():
            self.loadConfig()
        else:
            self.createConfig()
        self.createFolders()

    @staticmethod
    def createFolders():
        if not os.path.isdir('Profiles'):
            os.mkdir('Profiles')
        if not os.path.isdir('MyBrain'):
            os.mkdir('MyBrain')

    @staticmethod
    def checkConfig():
        if os.path.isfile('Config.ini'):
            config = open('Config.ini', 'r')
            lines = config.readlines()

            if len(lines) != len(t.configKeys):
                config.close()
                return False

            for line in lines:
                if not line[0:line.find(':')] in t.configKeys:
                    config.close()
                    return False

            config.close()
            return True

        else:
            return False

    def loadConfig(self):
        config = open('Config.ini', 'r')
        lines = config.readlines()

        for line in lines:
            key = line[0:line.find(':')]
            value = line[line.find(':') + 1:]

            if key == 'pName':
                if value:
                    value = value.replace('\n','')
                    t.programName = value
                else:
                    self.createConfig()

            elif key == 'pGender':
                if value.replace('\n', '') == "MALE":
                    t.agentVoice.setProperty('voice', t.agentVoice.getProperty('voices')[0].id)
                    t.agentGender = 'MALE'
                elif value.replace('\n', '') == "FEMALE":
                    t.agentVoice.setProperty('voice', t.agentVoice.getProperty('voices')[1].id)
                    t.agentGender = 'FEMALE'
                else:
                    self.createConfig()

            elif key == 'Camera':
                try:
                    t.cameraOn = bool(int(value))
                except:
                    t.cameraOn = False

        config.close()

    def createConfig(self):

        if f.askAcceptance('Your Buddy',
                           'Hi there\nI think that i am your buddy but i am missing some information about '
                           'myself\nWill you help ?'):

            name = ''

            while not name:
                name = f.getValueUsingUI('My name', 'Greet :)\n You want to help me\nAfter all my name is ...',
                                         'That is your name')

            gender = ''

            while not gender or (gender.upper() != 'MALE' and gender.upper() != 'FEMALE'):
                gender = f.getValueUsingUI('My Gender', 'Please type my Gender (Male,Female)\nWrite as it is')

            try:
                x = cv2.VideoCapture(0)

                if x.isOpened():
                    s, img = x.read()

                    t.cameraOn = s
                else:
                    t.cameraOn = False
            except:
                t.cameraOn = False

            file = open('Config.ini', 'w')
            file.write('pName:' + name + '\n')
            file.write('pGender:' + gender.upper() + '\n')
            file.write('Camera:' + str(int(t.cameraOn)) + '\n')
            file.close()

            t.programName = name

            if gender.upper() == "MALE":
                t.agentVoice.setProperty('voice', t.agentVoice.getProperty('voices')[0].id)
                t.agentGender = 'MALE'
            elif gender.upper() == "FEMALE":
                t.agentVoice.setProperty('voice', t.agentVoice.getProperty('voices')[1].id)
                t.agentGender = 'FEMALE'

            f.sayAndWait(f.getRandomFromList(t.finishSettings))

        else:
            f.stopProgram()


class OnLaunch(object):
    """
    Launching process
    """
    def launch(self):
        if f.checkFirstTime():
            f.createUser()
        else:
            f.sayRandom(t.welcome)
            f.sayAndWait("I am " + t.programName)

        self.initializeEvents()

    @staticmethod
    def initializeEvents():
        if not os.path.isdir('MyBrain'):
            f.sayRandom(t.error)
            f.sayAndWait('I have to close')
            f.stopProgram(1010)

        if not os.path.isfile('MyBrain/DailyEvents.ev'):
            t.dailyEvents = list()
        else:
            t.dailyEvents = f.loadFile('MyBrain/DailyEvents.ev')

        if not os.path.isfile('MyBrain/WeeklyEvents.ev'):
            t.weeklyEvents = list()
        else:
            t.weeklyEvents = f.loadFile('MyBrain/WeeklyEvents.ev')

        if not os.path.isfile('MyBrain/MonthlyEvents.ev'):
            t.monthlyEvents = list()
        else:
            t.monthlyEvents = f.loadFile('MyBrain/MonthlyEvents.ev')

        if not os.path.isfile('MyBrain/YearlyEvents.ev'):
            t.yearlyEvents = list()
        else:
            t.yearlyEvents = f.loadFile('MyBrain/YearlyEvents.ev')

        if not os.path.isfile('MyBrain/CustomEvents.ev'):
            t.customEvents = list()
        else:
            t.customEvents = f.loadFile('MyBrain/CustomEvents.ev')


class OnRun(object):
    def __init__(self):
        self.window = ui.MainWindow()
        self.isRunning = True
        self.filtered = False
        self.inStart = list()
        self.fiveMinutes = list()
        self.tenMinutes = list()
        self.fifteenMinutes = list()
        self.thirtyMinutes = list()
        self.oneHour = list()
        self.doneToday = list()
        self.today = '00-00-0000'

    def start(self):
        # Launch Thread for time management
        th.Thread(target=self.run, daemon=True).start()

        self.window.mainloop()

        while t.creatingProfile:
            f.createUser()
            self.window = ui.MainWindow()
            self.window.mainloop()

    def run(self):
        self.today = dt.datetime.now().strftime('%d-%m-%Y')
        while self.isRunning:
            now = dt.datetime.now().strftime('%H:%M')
            self.cycle(now)
            if not self.sameDay():
                self.doneToday.clear()

                if isinstance(t.currentProfile,t.c.Profile):
                    t.eventList = f.getToDayEvents(t.currentProfile.id)
                    t.eventListChanged = True
                    self.filtered = False

            time.sleep(5)

    def sameDay(self)->bool:
        now = dt.datetime.now().strftime('%d-%m-%Y')
        now = dt.datetime.strptime(now,'%d-%m-%Y')
        prev = dt.datetime.strptime(self.today,'%d-%m-%Y')

        if now > prev:
            return False

        return True

    def cycle(self,cycleTime:str):

        if t.eventListChanged:
            for event, status in t.eventList:
                if event.name in self.doneToday:
                    t.eventList.remove((event, status))
            t.eventListChanged = False

        if not isinstance(t.currentProfile,t.c.Profile):
            self.filtered = False
            return

        if isinstance(t.currentProfile,t.c.Profile):
            if not self.filtered:
                t.eventList = f.getToDayEvents(t.currentProfile.id)
                self.filtered = True
                t.eventsList = f.filterEvents(t.eventList,cycleTime)

            for event,notTime in t.eventList:

                remaining = f.calculateSeconds(event.time, cycleTime)

                if event.level == t.c.EventImportanceLevel.Basic:
                    if 60 <= remaining <= 600 and event.name not in self.tenMinutes:
                        f.sayEvent(event.name,event.des,"10 Minutes or less")
                        self.tenMinutes.append(event.name)
                    elif 0 <= remaining < 60:
                        f.sayEvent(event.name,event.des,"a few seconds")
                        t.eventList.remove((event,notTime))
                        if event.name in self.tenMinutes:
                            self.tenMinutes.remove(event.name)

                        self.doneToday.append(event.name)

                if event.level == t.c.EventImportanceLevel.Normal:
                    if 600 < remaining <= 3600 and event.name not in self.oneHour:
                        f.sayEvent(event.name,event.des,"1 Hour or even less")
                        self.oneHour.append(event.name)
                    if 60 <= remaining <= 600 and event.name not in self.tenMinutes:
                        f.sayEvent(event.name,event.des,"10 Minutes or less")
                        self.tenMinutes.append(event.name)
                    elif 0 <= remaining < 60:
                        f.sayEvent(event.name,event.des,"a few seconds")
                        t.eventList.remove((event,notTime))
                        if event.name in self.tenMinutes:
                            self.tenMinutes.remove(event.name)

                        if event.name in self.oneHour:
                            self.oneHour.remove(event.name)

                        self.doneToday.append(event.name)

                if event.level == t.c.EventImportanceLevel.Important:
                    if 1800 < remaining <= 3600 and event.name not in self.oneHour:
                        f.sayEvent(event.name, event.des, "1 Hour or even less")
                        self.oneHour.append(event.name)
                    elif 900 < remaining <= 1800 and event.name not in self.thirtyMinutes:
                        f.sayEvent(event.name, event.des, "half Hour or even less")
                        self.thirtyMinutes.append(event.name)
                    elif 600 < remaining <= 900 and event.name not in self.fifteenMinutes:
                        f.sayEvent(event.name, event.des, "15 Minutes or even less")
                        self.fifteenMinutes.append(event.name)
                    elif 180 <= remaining <= 600 and event.name not in self.tenMinutes:
                        f.sayEvent(event.name, event.des, "10 Minutes or less")
                        self.tenMinutes.append(event.name)
                    elif 60 <= remaining < 180 and event.name not in self.fiveMinutes:
                        f.sayEvent(event.name, event.des, "5 Minutes or less")
                        self.fiveMinutes.append(event.name)
                    elif 0 <= remaining < 60:
                        f.sayEvent(event.name, event.des, "a few seconds")
                        t.eventList.remove((event,notTime))
                        if event.name in self.tenMinutes:
                            self.tenMinutes.remove(event.name)

                        if event.name in self.oneHour:
                            self.oneHour.remove(event.name)

                        if event.name in self.fiveMinutes:
                            self.fiveMinutes.remove(event.name)

                        if event.name in self.fifteenMinutes:
                            self.fifteenMinutes.remove(event.name)

                        if event.name in self.thirtyMinutes:
                            self.thirtyMinutes.remove(event.name)

                        self.doneToday.append(event.name)

                if event.level == t.c.EventImportanceLevel.Critical:
                    if notTime:
                        f.sayAndWait(f.getRandomFromList(t.criticalEventTomorrow).format(x=event.name))
                        if event.des:
                            f.sayAndWait('This event you described as the following')
                            f.sayAndWait(event.des)

                        t.eventList.remove((event,True))
                        self.doneToday.append(event.name)
                    elif remaining > 3600 and event.name not in self.inStart:
                        f.sayEvent(event.name,event.des,'few hours')
                        self.inStart.append(event.name)
                    elif 1800 < remaining <= 3600 and event.name not in self.oneHour:
                        f.sayEvent(event.name, event.des, "1 Hour or even less")
                        self.oneHour.append(event.name)
                    elif 900 < remaining <= 1800 and event.name not in self.thirtyMinutes:
                        f.sayEvent(event.name, event.des, "half Hour or even less")
                        self.thirtyMinutes.append(event.name)
                    elif 600 < remaining <= 900 and event.name not in self.fifteenMinutes:
                        f.sayEvent(event.name, event.des, "15 Minutes or even less")
                        self.fifteenMinutes.append(event.name)
                    elif 180 <= remaining <= 600 and event.name not in self.tenMinutes:
                        f.sayEvent(event.name, event.des, "10 Minutes or less")
                        self.tenMinutes.append(event.name)
                    elif 60 <= remaining < 180 and event.name not in self.fiveMinutes:
                        f.sayEvent(event.name, event.des, "5 Minutes or less")
                        self.fiveMinutes.append(event.name)
                    elif 0 <= remaining < 60:
                        f.sayEvent(event.name, event.des, "a few seconds")
                        t.eventList.remove((event,notTime))
                        if event.name in self.tenMinutes:
                            self.tenMinutes.remove(event.name)

                        if event.name in self.oneHour:
                            self.oneHour.remove(event.name)

                        if event.name in self.fiveMinutes:
                            self.fiveMinutes.remove(event.name)

                        if event.name in self.fifteenMinutes:
                            self.fifteenMinutes.remove(event.name)

                        if event.name in self.thirtyMinutes:
                            self.thirtyMinutes.remove(event.name)

                        if event.name in self.inStart:
                            self.inStart.remove(event.name)

                        self.doneToday.append(event.name)
