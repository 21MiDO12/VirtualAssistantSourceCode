import pTypes as t
import functions as f
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import babel.numbers


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        t.creatingProfile = False
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(False, False)
        self.title(t.programName)
        self.geometry("500x500+300+200")
        self.wm_iconbitmap('VALogo.ico')
        self.frames = {}
        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.pack(side='top', fill='both', expand=True)
        for frame in (LoginPage, MainMenu, AddEvent, DailyEvent, WeeklyEvent, MonthlyEvent, YearlyEvent, CustomEvent,
                      Settings, Info):
            x = frame(container, self)
            self.frames[frame.__name__] = x
            x.grid(row=0, column=0, sticky='nsew')
        self.showFrame("LoginPage")

    def showFrame(self, pageName):
        self.frames[pageName].tkraise()


class LoginPage(tk.Frame):

    def cameraLogin(self):
        img = f.getInstantPhoto()

        f.checkProfile(img)

        if isinstance(t.currentProfile, t.c.Profile):
            f.sayAndWait(f.getRandomFromList(t.welcome) + " " + t.currentProfile.name)
            t.eventList = f.getToDayEvents(t.currentProfile.id)
            t.eventListChanged = True
            self.controller.showFrame('MainMenu')
        else:
            f.sayAndWait("Sorry i don't know you\nPlease create a profile")

        self.user.set('')
        self.password.set('')

    def userLogin(self):

        f.checkProfileUserAndPass(self.user.get(), self.password.get())

        if isinstance(t.currentProfile, t.c.Profile):
            f.sayAndWait(f.getRandomFromList(t.welcome) + " " + t.currentProfile.name)
            self.controller.showFrame('MainMenu')
        else:
            f.sayAndWait("Sorry i don't know you\nPlease create a profile")

        self.user.set('')
        self.password.set('')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.user = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(self, text=t.programName).pack()

        if t.cameraOn:
            tk.Button(self, text='Login using camera', command=self.cameraLogin).pack(pady=20)

        tk.Label(self, text='Username : ').pack()
        tk.Entry(self, textvariable=self.user).pack()
        tk.Label(self, text='Password : ').pack()
        tk.Entry(self, textvariable=self.password, show='*').pack()
        tk.Button(self, text='Login using user and pass', command=self.userLogin).pack(pady=20)


class MainMenu(tk.Frame):
    def backButton(self):
        if t.talking:
            return
        try:
            f.sayAndWait(f.getRandomFromList(t.exiting) + " " + t.currentProfile.name)
        except:
            return
        t.currentProfile = 0
        t.eventList.clear()
        t.eventListChanged = True
        self.controller.showFrame('LoginPage')

    def profileCreation(self):
        x = len(f.getAllProfiles())

        if x >= t.maxProfileNumber:
            f.sayAndWait('Sorry no user available\nplease try to call the developer for more users')
            f.sayAndWait('I think that is because your package\nyou may need to change it')
            return
        else:
            t.creatingProfile = True
            t.currentProfile = 0
            t.eventList.clear()
            t.eventListChanged = True
            self.controller.destroy()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text=t.programName + "'s Control Panel").pack(pady=10)
        tk.Button(self, text="Add Event", command=lambda: self.controller.showFrame('AddEvent')).pack()
        tk.Button(self, text="Create new profile", command=self.profileCreation).pack()
        tk.Button(self, text="Settings", command=lambda: self.controller.showFrame('Settings')).pack()
        tk.Button(self, text="Agent Information", command=lambda: self.controller.showFrame('Info')).pack()
        tk.Button(self, text="I'm out for sometime", command=self.backButton).pack()


class Info(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text=t.programName + "'s Information").pack(pady=10)
        tk.Label(self, text='Program still in BETA',fg='#f00').pack()
        tk.Label(self, text='Version : ' + t.version).pack()
        tk.Label(self, text='Dev Name : ' + t.creator).pack()
        tk.Label(self, text='Dev Email : ' + t.email).pack()
        tk.Label(self, text='Please, feel free to contact me for any feedback').pack()
        tk.Button(self, text="Back", command=lambda: self.controller.showFrame('MainMenu')).pack()


class Settings(tk.Frame):

    def changeSettings(self):
        name = self.name.get()
        gender = self.sex.get()

        if not name:
            print(name)
            return

        if gender.upper() != 'MALE' and gender.upper() != 'FEMALE':
            print(gender)
            return

        t.cameraOn = f.cameraTest()

        file = open('Config.ini', 'w')
        file.write('pName:' + t.programName + '\n')
        file.write('pGender:' + t.agentGender.upper() + '\n')
        file.write('Camera:' + str(int(t.cameraOn)) + '\n')
        file.close()

        t.programName = name

        if gender.upper() == "MALE":
            t.agentVoice.setProperty('voice', t.agentVoice.getProperty('voices')[0].id)
            t.agentGender = 'MALE'
        elif gender.upper() == "FEMALE":
            t.agentVoice.setProperty('voice', t.agentVoice.getProperty('voices')[1].id)
            t.agentGender = 'FEMALE'

        if not t.talking:
            f.sayAndWait('Then i am ' + name + " now")
        self.controller.showFrame('MainMenu')

    def cameraCheck(self):
        if f.cameraTest():
            t.cameraOn = True
            self.camStatus.set('Already have a camera set')
        else:
            t.cameraOn = False
            self.camStatus.set('No camera detected')

        file = open('Config.ini', 'w')
        file.write('pName:' + t.programName + '\n')
        file.write('pGender:' + t.agentGender.upper() + '\n')
        file.write('Camera:' + str(int(t.cameraOn)) + '\n')
        file.close()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name = tk.StringVar()
        self.name.set(t.programName)
        self.sex = tk.StringVar()
        self.sex.set(t.agentGender)

        self.camStatus = tk.StringVar()

        if t.cameraOn:
            self.camStatus.set('Already have a camera set')
        else:
            self.camStatus.set('No camera detected')

        tk.Label(self, text=t.programName + '\'s Settings').place(x=200, y=50)

        tk.Label(self, text='Agent Name : ').place(x=100, y=100)
        tk.Entry(self, textvariable=self.name).place(x=250, y=100)

        tk.Label(self, text='Agent Gender : ').place(x=100, y=150)
        ttk.Combobox(self, values=['MALE', 'FEMALE'], textvariable=self.sex).place(
            x=250, y=150)

        tk.Button(self, text='Camera Status : ',command=self.cameraCheck).place(x=100, y=200)
        tk.Label(self, width=25, textvariable=self.camStatus).place(x=250, y=200)

        tk.Button(self, text='Apply', command=self.changeSettings).place(x=250, y=250)
        tk.Button(self, text='Back', command=lambda: self.controller.showFrame('MainMenu')).place(x=300, y=250)


class AddEvent(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text=t.programName + '\'s Event Options').pack()
        tk.Button(self, text='Daily Event', command=lambda: self.controller.showFrame('DailyEvent')).pack()
        tk.Button(self, text='Weekly Event', command=lambda: self.controller.showFrame('WeeklyEvent')).pack()
        tk.Button(self, text='Monthly Event', command=lambda: self.controller.showFrame('MonthlyEvent')).pack()
        tk.Button(self, text='Yearly Event', command=lambda: self.controller.showFrame('YearlyEvent')).pack()
        tk.Button(self, text='Only once Event', command=lambda: self.controller.showFrame('CustomEvent')).pack()
        tk.Button(self, text='Back', command=lambda: self.controller.showFrame('MainMenu')).pack()


class DailyEvent(tk.Frame):

    def addEvent(self):
        name = self.name.get()
        des = self.des.get("1.0", "end-1c")
        level = self.level.get()
        min = self.timeMin.get()
        hour = self.timeHours.get()

        if not name:
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Name'))
            return

        if not (min and hour):
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Time'))
            return

        if int(min) < 0 or int(min) > 59:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Minutes can not be ' + min)
            return

        if int(hour) < 0 or int(hour) > 23:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Hours can not be ' + hour)
            return

        if level == 'Normal':
            level = t.c.EventImportanceLevel.Normal
        elif level == 'Critical':
            level = t.c.EventImportanceLevel.Critical
        elif level == 'Important':
            level = t.c.EventImportanceLevel.Important
        elif level == 'Just Remember':
            level = t.c.EventImportanceLevel.Basic
        else:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Importance Level can not be ' + level)
            return

        new = t.c.DailyEvent(name, "{x}:{y}".format(x=hour, y=min), t.currentProfile.id, level, des)

        f.insertEvent(new, t.c.EventType.Daily)

        f.sayRandom(t.finishSettings)
        f.sayAndWait(f.getRandomFromList(t.dailyEventStored).format(x=name))

        if isinstance(t.currentProfile, t.c.Profile):
            t.eventList = f.getToDayEvents(t.currentProfile.id)
            t.eventListChanged = True

        self.controller.showFrame('MainMenu')
        self.name.set('')
        self.des.delete("1.0", "end-1c")
        self.timeMin.set('')
        self.timeHours.set('')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name = tk.StringVar()
        self.level = tk.StringVar()
        self.level.set('Normal')
        self.timeMin = tk.StringVar()
        self.timeHours = tk.StringVar()

        tk.Label(self, text='Create Daily Event').place(x=200, y=50)

        tk.Label(self, text='Event Name : ').place(x=100, y=100)
        tk.Entry(self, textvariable=self.name).place(x=250, y=100)

        tk.Label(self, text='Event Importance Level : ').place(x=100, y=150)
        ttk.Combobox(self, values=['Critical', 'Important', 'Normal', 'Just Remember'], textvariable=self.level).place(
            x=250, y=150)

        tk.Label(self, text='Event Description : ').place(x=100, y=200)
        self.des = tk.Text(self, width=25)
        self.des.place(x=250, y=200, height=90)

        tk.Label(self, text='Event Time : ').place(x=100, y=300)
        tk.Spinbox(self, from_=0, to=23, textvariable=self.timeHours).place(x=250, y=300, width=100, height=30)
        tk.Spinbox(self, from_=0, to=59, textvariable=self.timeMin).place(x=350, y=300, width=100, height=30)

        tk.Button(self, text='Store', command=self.addEvent).place(x=250, y=350)
        tk.Button(self, text='Back', command=lambda: self.controller.showFrame('MainMenu')).place(x=300, y=350)


class WeeklyEvent(tk.Frame):

    def addEvent(self):
        name = self.name.get()
        des = self.des.get("1.0", "end-1c")
        level = self.level.get()
        min = self.timeMin.get()
        hour = self.timeHours.get()
        days = [x.get() for x in self.days]

        if not name:
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Name'))
            return

        if not (min and hour):
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Time'))
            return

        if not min.isnumeric():
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Minutes definitely can not be ' + min)
            return

        if not hour.isnumeric():
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Hours definitely can not be ' + hour)
            return

        if int(min) < 0 or int(min) > 59:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Minutes can not be ' + min)
            return

        if int(hour) < 0 or int(hour) > 23:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Hours can not be ' + hour)
            return

        if level == 'Normal':
            level = t.c.EventImportanceLevel.Normal
        elif level == 'Critical':
            level = t.c.EventImportanceLevel.Critical
        elif level == 'Important':
            level = t.c.EventImportanceLevel.Important
        elif level == 'Just Remember':
            level = t.c.EventImportanceLevel.Basic
        else:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Importance Level can not be ' + level)
            return

        if not 1 in days:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait("What a weekly event does not happen in the week")
            return

        for day in enumerate(days):
            if day[1]:
                new = t.c.WeeklyEvent(name, "{x}:{y}".format(x=hour, y=min), self.daysNames[day[0]], t.currentProfile.id
                                      , level, des)

                f.insertEvent(new, t.c.EventType.Weekly)

        for e in f.loadFile('MyBrain/WeeklyEvents.ev'):
            print(e)

        f.sayRandom(t.finishSettings)
        f.sayAndWait(f.getRandomFromList(t.weeklyEventStored).format(x=name))

        if isinstance(t.currentProfile, t.c.Profile):
            t.eventList = f.getToDayEvents(t.currentProfile.id)
            t.eventListChanged = True

        self.controller.showFrame('MainMenu')
        self.name.set('')
        self.des.delete("1.0", "end-1c")
        self.timeMin.set('0')
        self.timeHours.set('0')

        for day in self.days:
            day.set(0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name = tk.StringVar()
        self.level = tk.StringVar()
        self.level.set('Normal')
        self.timeMin = tk.StringVar()
        self.timeHours = tk.StringVar()
        self.days = [tk.IntVar(0) for i in range(7)]

        tk.Label(self, text='Create Weekly Event').place(x=200, y=50)

        tk.Label(self, text='Event Name : ').place(x=100, y=100)
        tk.Entry(self, textvariable=self.name).place(x=250, y=100)

        tk.Label(self, text='Event Importance Level : ').place(x=100, y=150)
        ttk.Combobox(self, values=['Critical', 'Important', 'Normal', 'Just Remember'], textvariable=self.level).place(
            x=250, y=150)

        self.daysNames = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        tk.Label(self, text='Event Day : ').place(x=240, y=200)
        for i in range(7):
            if i < 5:
                tk.Checkbutton(self, text=self.daysNames[i], variable=self.days[i], onvalue=1, offvalue=0, height=2,
                               width=10).place(x=i * 100 + 5, y=200)
            else:
                tk.Checkbutton(self, text=self.daysNames[i], variable=self.days[i], onvalue=1, offvalue=0, height=2,
                               width=10).place(x=(i % 5) * 100 + 5, y=250)

        tk.Label(self, text='Event Description : ').place(x=100, y=300)
        self.des = tk.Text(self, width=25)
        self.des.place(x=250, y=300, height=90)

        tk.Label(self, text='Event Time : ').place(x=100, y=400)
        tk.Spinbox(self, from_=0, to=23, textvariable=self.timeHours).place(x=250, y=400, width=100, height=30)
        tk.Spinbox(self, from_=0, to=59, textvariable=self.timeMin).place(x=350, y=400, width=100, height=30)

        tk.Button(self, text='Store', command=self.addEvent).place(x=250, y=450)
        tk.Button(self, text='Back', command=lambda: self.controller.showFrame('MainMenu')).place(x=300, y=450)


class MonthlyEvent(tk.Frame):

    def addEvent(self):
        name = self.name.get()
        des = self.des.get("1.0", "end-1c")
        level = self.level.get()
        min = self.timeMin.get()
        hour = self.timeHours.get()

        if not self.day.get().isnumeric():
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Event day can not be ' + self.day.get())
            return

        day = int(self.day.get())

        if not name:
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Name'))
            return

        if not (min and hour):
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Time'))
            return

        if int(min) < 0 or int(min) > 59:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Minutes can not be ' + min)
            return

        if int(hour) < 0 or int(hour) > 23:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Hours can not be ' + hour)
            return

        if level == 'Normal':
            level = t.c.EventImportanceLevel.Normal
        elif level == 'Critical':
            level = t.c.EventImportanceLevel.Critical
        elif level == 'Important':
            level = t.c.EventImportanceLevel.Important
        elif level == 'Just Remember':
            level = t.c.EventImportanceLevel.Basic
        else:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Importance Level can not be ' + level)
            return

        if not day or day < 1 or day > 31:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('How do i suppose to know the day')
            return

        new = t.c.MonthlyEvent(name, "{x}:{y}".format(x=hour, y=min), day, t.currentProfile.id
                               , level, des)

        f.insertEvent(new, t.c.EventType.Monthly)

        for e in f.loadFile('MyBrain/MonthlyEvents.ev'):
            print(e)

        f.sayRandom(t.finishSettings)
        f.sayAndWait(f.getRandomFromList(t.monthlyEventStored).format(x=name))

        if isinstance(t.currentProfile, t.c.Profile):
            t.eventList = f.getToDayEvents(t.currentProfile.id)
            t.eventListChanged = True

        self.controller.showFrame('MainMenu')
        self.name.set('')
        self.des.delete("1.0", "end-1c")
        self.timeMin.set('0')
        self.timeHours.set('0')
        self.day.set('1')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text='Create Monthly Event').place(x=200, y=50)

        self.name = tk.StringVar()
        self.level = tk.StringVar()
        self.level.set('Normal')
        self.timeMin = tk.StringVar()
        self.timeHours = tk.StringVar()
        self.day = tk.StringVar()
        self.day.set('1')

        tk.Label(self, text='Event Name : ').place(x=100, y=100)
        tk.Entry(self, textvariable=self.name).place(x=250, y=100)

        tk.Label(self, text='Event Importance Level : ').place(x=100, y=150)
        ttk.Combobox(self, values=['Critical', 'Important', 'Normal', 'Just Remember'], textvariable=self.level).place(
            x=250, y=150)

        tk.Label(self, text='Event Day : ').place(x=100, y=200)
        ttk.Combobox(self, values=[str(i) for i in range(1, 32)], textvariable=self.day).place(x=250, y=200)

        tk.Label(self, text='Event Description : ').place(x=100, y=250)
        self.des = tk.Text(self, width=25)
        self.des.place(x=250, y=250, height=90)

        tk.Label(self, text='Event Time : ').place(x=100, y=350)
        tk.Spinbox(self, from_=0, to=23, textvariable=self.timeHours).place(x=250, y=350, width=100, height=30)
        tk.Spinbox(self, from_=0, to=59, textvariable=self.timeMin).place(x=350, y=350, width=100, height=30)

        tk.Button(self, text='Store', command=self.addEvent).place(x=250, y=400)
        tk.Button(self, text='Back', command=lambda: self.controller.showFrame('MainMenu')).place(x=300, y=400)


class YearlyEvent(tk.Frame):

    def addEvent(self):
        name = self.name.get()
        des = self.des.get("1.0", "end-1c")
        level = self.level.get()
        min = self.timeMin.get()
        hour = self.timeHours.get()

        if not self.day.get().isnumeric():
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Event day can not be ' + self.day.get())
            return

        if not self.month.get().isnumeric():
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Event day can not be ' + self.day.get())
            return

        day = int(self.day.get())
        month = int(self.month.get())

        if not name:
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Name'))
            return

        if not (min and hour):
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Time'))
            return

        if int(min) < 0 or int(min) > 59:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Minutes can not be ' + min)
            return

        if int(hour) < 0 or int(hour) > 23:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Hours can not be ' + hour)
            return

        if level == 'Normal':
            level = t.c.EventImportanceLevel.Normal
        elif level == 'Critical':
            level = t.c.EventImportanceLevel.Critical
        elif level == 'Important':
            level = t.c.EventImportanceLevel.Important
        elif level == 'Just Remember':
            level = t.c.EventImportanceLevel.Basic
        else:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Importance Level can not be ' + level)
            return

        if not day or day < 1 or day > 31:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('How do i suppose to know the day')
            return

        if not month or month < 1 or month > 12:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('How do i suppose to know the month')
            return

        new = t.c.YearlyEvent(name, "{x}:{y}".format(x=hour, y=min), day, month, t.currentProfile.id
                              , level, des)

        f.insertEvent(new, t.c.EventType.Yearly)

        for e in f.loadFile('MyBrain/YearlyEvents.ev'):
            print(e)

        f.sayRandom(t.finishSettings)
        f.sayAndWait(f.getRandomFromList(t.yearlyEventStored).format(x=name))

        if isinstance(t.currentProfile, t.c.Profile):
            t.eventList = f.getToDayEvents(t.currentProfile.id)
            t.eventListChanged = True

        self.controller.showFrame('MainMenu')
        self.name.set('')
        self.des.delete("1.0", "end-1c")
        self.timeMin.set('0')
        self.timeHours.set('0')
        self.day.set('1')
        self.month.set('1')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text='Create Yearly Event').place(x=200, y=50)

        self.name = tk.StringVar()
        self.level = tk.StringVar()
        self.level.set('Normal')
        self.timeMin = tk.StringVar()
        self.timeHours = tk.StringVar()
        self.day = tk.StringVar()
        self.day.set('1')
        self.month = tk.StringVar()
        self.month.set('1')

        tk.Label(self, text='Event Name : ').place(x=100, y=100)
        tk.Entry(self, textvariable=self.name).place(x=250, y=100)

        tk.Label(self, text='Event Importance Level : ').place(x=100, y=150)
        ttk.Combobox(self, values=['Critical', 'Important', 'Normal', 'Just Remember'], textvariable=self.level).place(
            x=250, y=150)

        tk.Label(self, text='Event Day : ').place(x=100, y=200)
        ttk.Combobox(self, values=[str(i) for i in range(1, 32)], textvariable=self.day).place(x=250, y=200)

        tk.Label(self, text='Event Month : ').place(x=100, y=250)
        ttk.Combobox(self, values=[str(i) for i in range(1, 13)], textvariable=self.month).place(x=250, y=250)

        tk.Label(self, text='Event Description : ').place(x=100, y=300)
        self.des = tk.Text(self, width=25)
        self.des.place(x=250, y=300, height=90)

        tk.Label(self, text='Event Time : ').place(x=100, y=400)
        tk.Spinbox(self, from_=0, to=23, textvariable=self.timeHours).place(x=250, y=400, width=100, height=30)
        tk.Spinbox(self, from_=0, to=59, textvariable=self.timeMin).place(x=350, y=400, width=100, height=30)

        tk.Button(self, text='Store', command=self.addEvent).place(x=250, y=450)
        tk.Button(self, text='Back', command=lambda: self.controller.showFrame('MainMenu')).place(x=300, y=450)


class CustomEvent(tk.Frame):
    def addEvent(self):
        name = self.name.get()
        des = self.des.get("1.0", "end-1c")
        level = self.level.get()
        min = self.timeMin.get()
        hour = self.timeHours.get()
        date = self.date.get()

        if not name:
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Name'))
            return

        if not (min and hour):
            f.sayAndWait(f.getRandomFromList(t.needing).format(x='Event Time'))
            return

        if int(min) < 0 or int(min) > 59:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Minutes can not be ' + min)
            return

        if int(hour) < 0 or int(hour) > 23:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Hours can not be ' + hour)
            return

        if level == 'Normal':
            level = t.c.EventImportanceLevel.Normal
        elif level == 'Critical':
            level = t.c.EventImportanceLevel.Critical
        elif level == 'Important':
            level = t.c.EventImportanceLevel.Important
        elif level == 'Just Remember':
            level = t.c.EventImportanceLevel.Basic
        else:
            f.sayRandom(t.youAreKidding)
            f.sayAndWait('Importance Level can not be ' + level)
            return

        new = t.c.CustomEvent(name, "{x}:{y}".format(x=hour, y=min), date, t.currentProfile.id
                              , level, des)

        f.insertEvent(new, t.c.EventType.Custom)

        for e in f.loadFile('MyBrain/CustomEvents.ev'):
            print(e)

        f.sayRandom(t.finishSettings)
        f.sayAndWait(f.getRandomFromList(t.customEventStored).format(x=name))

        if isinstance(t.currentProfile, t.c.Profile):
            t.eventList = f.getToDayEvents(t.currentProfile.id)
            t.eventListChanged = True

        self.controller.showFrame('MainMenu')
        self.name.set('')
        self.des.delete("1.0", "end-1c")
        self.timeMin.set('0')
        self.timeHours.set('0')
        self.date.set('')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text='Create Only Once Event').place(x=200, y=50)

        self.name = tk.StringVar()
        self.level = tk.StringVar()
        self.level.set('Normal')
        self.timeMin = tk.StringVar()
        self.timeHours = tk.StringVar()
        self.date = tk.StringVar()

        tk.Label(self, text='Event Name : ').place(x=100, y=100)
        tk.Entry(self, textvariable=self.name).place(x=250, y=100)

        tk.Label(self, text='Event Importance Level : ').place(x=100, y=150)
        ttk.Combobox(self, values=['Critical', 'Important', 'Normal', 'Just Remember'], textvariable=self.level).place(
            x=250, y=150)

        tk.Label(self, text='Event Date : ').place(x=100, y=200)
        DateEntry(self, width=12, background='darkblue', bd=1, foreground='white',
                  borderwidth=2, textvariable=self.date, date_pattern='dd-mm-y').place(x=250, y=200)

        tk.Label(self, text='Event Description : ').place(x=100, y=250)
        self.des = tk.Text(self, width=25)
        self.des.place(x=250, y=250, height=90)

        tk.Label(self, text='Event Time : ').place(x=100, y=400)
        tk.Spinbox(self, from_=0, to=23, textvariable=self.timeHours).place(x=250, y=350, width=100, height=30)
        tk.Spinbox(self, from_=0, to=59, textvariable=self.timeMin).place(x=350, y=350, width=100, height=30)

        tk.Button(self, text='Store', command=self.addEvent).place(x=250, y=400)
        tk.Button(self, text='Back', command=lambda: self.controller.showFrame('MainMenu')).place(x=300, y=400)
