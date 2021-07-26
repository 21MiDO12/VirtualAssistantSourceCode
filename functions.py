import pTypes as t
import os
import glob
import tkinter as tk
import cv2
import dlib
import face_recognition as fr
import pickle
import datetime as dt
from imutils import face_utils
from random import randint
from time import sleep


def sayAndWait(text: str):
    c = 0
    while t.talking:
        c += 1
        if c > 5:
            t.talking = False
        sleep(1)

    if t.talking:
        return
    t.talking = True

    if t.agentVoice._inLoop:
        t.agentVoice.stop()

    t.agentVoice.say(text)
    t.agentVoice.runAndWait()
    t.talking = False


def sayRandom(allSpeech: list):
    sayAndWait(getRandomFromList(allSpeech))


def sayEvent(eventName: str, eventDes: str, remainingTime: str):
    sayAndWait(getRandomFromList(t.eventAfterTime).format(x=eventName, y=remainingTime))

    if eventDes:
        sayAndWait("Be aware that you said also about " + eventName + " the following")
        sayAndWait(eventDes)

    sayAndWait(t.currentProfile.name)
    sayRandom(t.hopeBest)


def cameraTest() -> bool:
    try:
        x = cv2.VideoCapture(0)

        if x.isOpened():
            s, img = x.read()

            return s
        else:
            return False
    except:
        return False


def checkFirstTime() -> bool:
    """Check if there's profile or not"""
    if os.path.isdir('Profiles'):
        if not glob.glob('Profiles/*'):
            return True
        else:
            return False
    else:
        return True


def takePicture(message: str = '', cropFace=False):
    cam = cv2.VideoCapture(0)
    det = dlib.get_frontal_face_detector()

    good = False

    img = 0
    while not good:
        while cv2.waitKey(1) < 0:
            s, img = cam.read()
            face = det(img)
            if face:
                face = face[0]
                x, y, w, h = face_utils.rect_to_bb(face)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow('Camera', img)

        cv2.destroyWindow('Camera')
        if not s or s is None:
            continue

        if not face:
            sayAndWait('Nobody in this picture\nplease try again')
            continue

        sayAndWait("That's the required picture\nAm i right?")
        cv2.imshow(message, img)
        cv2.waitKey(1)
        if askAcceptance(t.programName, 'That is the required?', 'Yes', 'No'):
            good = True
        else:
            cv2.destroyWindow(message)

    cv2.destroyAllWindows()

    if cropFace:
        try:
            img = img[y:y + w, x:x + h]
        except:
            sayRandom(t.error)

    return img


def getdiscriptors(face):
    return fr.face_encodings(face)[0]


def stopProgram(exitCode: int = 0):
    """
    This function closes the program
    :param exitCode: 0 means exit successfully
                    1010 means closed because the user deleted the myBrain folder before finishing the launch
                    50 means eventObject is not instance of Daily Event
                    51 means eventObject is not instance of Weekly Event
                    52 means eventObject is not instance of Monthly Event
                    53 means eventObject is not instance of Yearly Event
                    54 means eventObject is not instance of Custom Event
                    10 means importance level in daily event creation was wrong
    """
    try:
        exit(exitCode)
    except Exception:
        try:
            import sys
            sys.exit(exitCode)
        except:
            quit(exitCode)


def getValueUsingUI(title: str = 'Your Buddy Says', message: str = '', buttonMessage: str = 'Submit') -> str:
    def returnValue():
        window.destroy()

    window = tk.Tk()
    value = tk.StringVar()
    window.title(title)
    window.wm_iconbitmap('VALogo.ico')
    window.geometry("500x500+500+250")
    tk.Label(window, text=message).pack()
    tk.Entry(window, textvariable=value).pack()
    tk.Button(window, text=buttonMessage, command=returnValue).pack()

    window.mainloop()
    return value.get()


def askAcceptance(title: str = 'Your Buddy Says', message: str = '', okText: str = 'Ok',
                  cancelText: str = 'Cancel') -> bool:
    def returnTrue():
        value.set(True)
        window.destroy()

    def returnFalse():
        value.set(False)
        window.destroy()

    window = tk.Tk()
    value = tk.BooleanVar()
    window.title(title)
    window.wm_iconbitmap('VALogo.ico')
    window.geometry("500x500+500+250")
    tk.Label(window, text=message).pack()
    frame = tk.Frame(window)
    tk.Button(frame, text=okText, command=returnTrue).grid(row=0, column=0)
    tk.Button(frame, text=cancelText, command=returnFalse).grid(row=0, column=1)

    frame.pack()

    window.mainloop()
    return value.get()


def getRandomFromList(allData: list):
    return allData[randint(0, len(allData) - 1)]


def storeFile(obj, filename: str):
    pickle.dump(obj, open(filename, 'wb'))


def loadFile(filename: str):
    return pickle.load(open(filename, 'rb'))


def getId() -> int:
    if not os.path.isfile('MyBrain/Ids.data'):
        return 0

    x = loadFile('MyBrain/Ids.data')
    return len(x)


def storeID(profileId: int):
    if os.path.isfile('MyBrain/Ids.data'):
        x = loadFile('MyBrain/Ids.data')
        x.append(profileId)
        storeFile(x, 'MyBrain/Ids.data')
    else:
        x = []
        x.append(profileId)
        storeFile(x, 'MyBrain/Ids.data')


def getInstantPhoto():
    cam = cv2.VideoCapture(0)

    s, img = cam.read()

    while not s:
        s, img = cam.read()

    return img


def getAllProfiles():
    profiles = glob.glob('Profiles/Profile *.prof')

    result = []

    for profile in profiles:
        result.append(loadFile(profile))

    return result


def checkProfile(image):
    det = dlib.get_frontal_face_detector()
    faces = det(image)
    profiles = getAllProfiles()

    found = False

    for face in faces:
        x, y, w, h = face_utils.rect_to_bb(face)
        img = image[y:y + w, x:x + h]

        encoding = fr.face_encodings(img)

        if encoding:

            for profile in profiles:
                if fr.compare_faces(profile.encoding, encoding)[0]:
                    t.currentProfile = profile
                    found = True
                    break
            if found:
                break


def checkProfileUserAndPass(user: str, password: str):
    profiles = getAllProfiles()
    for profile in profiles:
        if profile.user == user and profile.password == password:
            t.currentProfile = profile
            break


def insertEvent(eventObject, eventType: t.c.EventType):
    if eventType == t.c.EventType.Daily:
        if not isinstance(eventObject, t.c.DailyEvent):
            sayRandom(t.error)
            sayAndWait('I have to close please report the developer')
            stopProgram(50)

        t.dailyEvents.append(eventObject)
        storeFile(t.dailyEvents, 'MyBrain/DailyEvents.ev')

    elif eventType == t.c.EventType.Weekly:
        if not isinstance(eventObject, t.c.WeeklyEvent):
            sayRandom(t.error)
            sayAndWait('I have to close please report the developer')
            stopProgram(51)

        t.weeklyEvents.append(eventObject)
        storeFile(t.weeklyEvents, 'MyBrain/WeeklyEvents.ev')

    elif eventType == t.c.EventType.Monthly:
        if not isinstance(eventObject, t.c.MonthlyEvent):
            sayRandom(t.error)
            sayAndWait('I have to close please report the developer')
            stopProgram(52)

        t.monthlyEvents.append(eventObject)
        storeFile(t.monthlyEvents, 'MyBrain/MonthlyEvents.ev')

    elif eventType == t.c.EventType.Yearly:
        if not isinstance(eventObject, t.c.YearlyEvent):
            sayRandom(t.error)
            sayAndWait('I have to close please report the developer')
            stopProgram(53)

        t.yearlyEvents.append(eventObject)
        storeFile(t.yearlyEvents, 'MyBrain/YearlyEvents.ev')

    elif eventType == t.c.EventType.Custom:
        if not isinstance(eventObject, t.c.CustomEvent):
            sayRandom(t.error)
            sayAndWait('I have to close please report the developer')
            stopProgram(54)

        t.customEvents.append(eventObject)
        storeFile(t.customEvents, 'MyBrain/CustomEvents.ev')


def debugFiles():
    if os.path.isfile('MyBrain/DailyEvents.ev'):
        print('DailyEvents')
        for e in loadFile('MyBrain/DailyEvents.ev'):
            print(e)
    else:
        print('Daily Events : None')

    if os.path.isfile('MyBrain/WeeklyEvents.ev'):
        print('WeeklyEvents')
        for e in loadFile('MyBrain/WeeklyEvents.ev'):
            print(e)
    else:
        print('Weekly Events : None')

    if os.path.isfile('MyBrain/MonthlyEvents.ev'):
        print('MonthlyEvents')
        for e in loadFile('MyBrain/MonthlyEvents.ev'):
            print(e)
    else:
        print('Monthly Events : None')

    if os.path.isfile('MyBrain/YearlyEvents.ev'):
        print('YearlyEvents')
        for e in loadFile('MyBrain/YearlyEvents.ev'):
            print(e)
    else:
        print('Yearly Events : None')

    if os.path.isfile('MyBrain/CustomEvents.ev'):
        print('CustomEvents')
        for e in loadFile('MyBrain/CustomEvents.ev'):
            print(e)
    else:
        print('Custom Events : None')


def getDayBefore(day: str) -> str:
    days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    x = days.index(day)

    if x == 0:
        return 'Friday'
    else:
        return days[x - 1]


def getToDayEvents(profileNumber: int) -> list:
    result = list()

    for event in t.dailyEvents:
        if event.userID == profileNumber:
            result.append((event, False))

    now = dt.datetime.now()

    factor = now.strftime('%A')

    for event in t.weeklyEvents:
        if event.day == factor and profileNumber == event.userID:
            result.append((event, False))
        elif event.level == t.c.EventImportanceLevel.Critical and factor == getDayBefore(event.day) \
                and profileNumber == event.userID:
            result.append((event, True))

    factor = int(now.strftime('%d'))

    for event in t.monthlyEvents:
        if event.day == factor and profileNumber == event.userID:
            result.append((event, False))
        elif event.level == t.c.EventImportanceLevel.Critical and factor == event.day - 1 \
                and profileNumber == event.userID:
            result.append((event, True))

    factor = (int(now.strftime('%d')), int(now.strftime('%m')))

    for event in t.yearlyEvents:
        if event.day == factor[0] and event.month == factor[1] and profileNumber == event.userID:
            result.append((event, False))
        elif event.level == t.c.EventImportanceLevel.Critical and factor[0] == event.day - 1 and factor[
            1] == event.month \
                and profileNumber == event.userID:
            result.append((event, True))

    factor = now.strftime('%d-%m-%Y')

    for event in t.customEvents:
        x = dt.datetime.strptime(factor, '%d-%m-%Y')
        y = dt.datetime.strptime(event.date, '%d-%m-%Y')
        if factor == event.date and event.userID == profileNumber:
            result.append((event, False))
        elif event.level == t.c.EventImportanceLevel.Critical and (y - x).total_seconds() == 86400 \
                and profileNumber == event.userID:
            result.append((event, True))

    return result


def calculateSeconds(x: str, y: str) -> int:
    x = x.split(':')
    y = y.split(':')

    return (int(x[0]) - int(y[0])) * 3600 + (int(x[1]) - int(y[1])) * 60


def filterEvents(events: list, timeNow: str, secondsTreshold=1) -> list:
    result = list()

    for event, status in events:
        if calculateSeconds(event.time, timeNow) > secondsTreshold and status:
            result.append(event)

    return result


def createUser():
    sayRandom(t.welcome)
    sayAndWait("I am " + t.programName)
    sayAndWait("It seems to me we don't know each other")
    sayAndWait("Then let's have a little knowledge about each other")
    sayAndWait("I've just started by introducing my self and i hope u will tell me your name")
    if not os.path.isdir('Profiles'):
        os.mkdir('Profiles/')

    name = getValueUsingUI('Your name', 'Please tell me your name')

    while not name:
        sayAndWait("Sorry, i didn't get your name correctly\nplease try again")
        name = getValueUsingUI('Your name', 'Please tell me your name')

    sayAndWait("Great , Your name is " + name + "\n now let's get to age\nMy age is")
    sayAndWait(getRandomFromList(t.agentAge))
    sayAndWait('After all tell me yours')

    age = getValueUsingUI('your age', 'Please tell me your age')

    while not age or not age.isnumeric():
        sayAndWait("Sorry, i didn't get your age correctly\nplease try again")
        age = getValueUsingUI('Your name', 'Please tell me your age')

    while int(age) < 10 or not age or not age.isnumeric() or int(age) > 70:
        sayRandom(t.youAreKidding)
        sayAndWait("What is your age again?")
        age = getValueUsingUI('Your name', 'Please tell me your real valid age\nBetween 10 and 70...')
        if not age:
            age = 0

    age = int(age)

    if 10 <= age < 20:
        sayAndWait('You are pretty young')
    elif 20 <= age < 30:
        sayAndWait('that is the feeling of being youth')
    elif 30 <= age < 50:
        sayAndWait('Greetings sir ' + name + '\nyou should have a greet life')
    elif 50 <= age <= 70:
        sayAndWait('then you are my grandpa\nwe should discuss some stories of your greet life some day')
    else:
        sayAndWait("I don't know how is this happening but you should know that there is something wrong")

    sayAndWait("Now you should know that i am bot\n so sometimes i am male and sometimes i am female")
    sayAndWait("But i don't know your sex so please tell me")

    gender = getValueUsingUI('Your Sex', 'please tell me your gender whether it is male or female')

    while gender.upper() != 'MALE' and gender.upper() != 'FEMALE':
        sayAndWait("Sorry, i didn't get your sex correctly\nplease try again")
        gender = getValueUsingUI('Your name', 'Please tell me that you are male or female')

    face = ''
    if t.cameraOn:
        sayAndWait('I will be glad if i know you better\n so please i want to take a picture of you'
                   '\npress any key when you are ready and i will take a picture for you')
        try:
            face = takePicture("Is that you?", cropFace=True)
            face = getdiscriptors(face)
        except:
            t.cameraOn = False

    sayAndWait("I'm glad to see you\nwe all most done\nlast thing i want to ask is a username and password"
               "\nplease be aware that if i couldn't recognize you at anytime\n"
               "you will be able to tell me that it is you by the username and password"
               "\nSo choose them carefully and wisely")

    user = getValueUsingUI(t.programName, "Your username\nCan't be empty\nCan have anything you want"
                                          "\nMake it short for you to remember", "Store Username")

    while not user:
        sayAndWait("Sorry, but you have to type username")
        user = getValueUsingUI(t.programName, "Your username\nCan't be empty\nCan have anything you want"
                                              "\nMake it short for you to remember", "Store Username")

    password = getValueUsingUI(t.programName, "Your Password\nCan't be empty\nCan have anything you want"
                                              "\ntry your best to remember it", "Store Password")

    newProfile = t.c.Profile(getId(), name, age, gender.upper(), user, password, face)
    storeFile(newProfile, 'Profiles/Profile ' + str(newProfile.id) + '.prof')
    storeID(newProfile.id)

    t.currentProfile = newProfile

    sayRandom(t.finishSettings)
