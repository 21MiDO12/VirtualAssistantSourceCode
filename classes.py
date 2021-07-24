import enum


class Profile(object):
    def __init__(self, id: int, name: str, age: int, gender: str, user: str, password: str, encodings):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.user = user
        self.password = password
        self.encoding = encodings

    def __str__(self):
        return str(self.id) + " " + self.name + " " + str(self.age) + " " + self.gender + " " + self.user + " " \
               + self.password


class EventImportanceLevel(enum.Enum):
    Critical = 0  # Recommend from the start of the day/Recommend every hour/Recommend in the day before the event
    Important = 1  # Recommend Before it start by (60m 30m 15m 10m 5m 1m)
    Normal = 2  # Recommend Before it start by (60m 10m 1m)
    Basic = 3  # Recommend Before it start by (10m 1m)


class EventType(enum.Enum):
    Daily = 0
    Weekly = 1
    Monthly = 2
    Yearly = 3
    Custom = 4


class DailyEvent(object):
    def __init__(self, eventName: str, eventTime: str, user: int, importance: EventImportanceLevel, eventDes: str = ''):
        self.name = eventName
        self.des = eventDes
        self.time = eventTime
        self.userID = user
        self.level = importance

    def __str__(self):
        x = dict()
        x['name'] = self.name
        x['time'] = self.time
        x['User'] = self.userID
        x['Importance'] = self.level
        x['description'] = self.des
        return str(x)

    def timeToSeconds(self):
        x = self.time.split(':')
        return x[0] * 3600 + x[1] * 60


class WeeklyEvent(object):
    def __init__(self, eventName: str, eventTime: str, weekDay: str, user: int, importance: EventImportanceLevel,
                 eventDes: str = ''):
        self.name = eventName
        self.des = eventDes
        self.time = eventTime
        self.userID = user
        self.level = importance
        self.day = weekDay

    def __str__(self):
        x = dict()
        x['name'] = self.name
        x['time'] = self.time
        x['User'] = self.userID
        x['Importance'] = self.level
        x['Day'] = self.day
        x['description'] = self.des
        return str(x)

    def timeToSeconds(self):
        x = self.time.split(':')
        return x[0] * 3600 + x[1] * 60


class MonthlyEvent(object):
    def __init__(self, eventName: str, eventTime: str, monthDay: int, user: int, importance: EventImportanceLevel,
                 eventDes: str = ''):
        self.name = eventName
        self.des = eventDes
        self.time = eventTime
        self.userID = user
        self.level = importance
        self.day = monthDay

    def __str__(self):
        x = dict()
        x['name'] = self.name
        x['time'] = self.time
        x['User'] = self.userID
        x['Importance'] = self.level
        x['Day'] = self.day
        x['description'] = self.des
        return str(x)

    def timeToSeconds(self):
        x = self.time.split(':')
        return x[0] * 3600 + x[1] * 60


class YearlyEvent(object):
    def __init__(self, eventName: str, eventTime: str, day: int, month: int, user: int,
                 importance: EventImportanceLevel, eventDes: str = ''):
        self.name = eventName
        self.des = eventDes
        self.time = eventTime
        self.userID = user
        self.level = importance
        self.day = day
        self.month = month

    def __str__(self):
        x = dict()
        x['name'] = self.name
        x['time'] = self.time
        x['User'] = self.userID
        x['Importance'] = self.level
        x['Date'] = str(self.day) + ":" + str(self.month)
        x['description'] = self.des
        return str(x)

    def timeToSeconds(self):
        x = self.time.split(':')
        return x[0] * 3600 + x[1] * 60


class CustomEvent(object):
    def __init__(self, eventName: str, eventTime: str, date: str, user: int, importance: EventImportanceLevel,
                 eventDes: str = ''):
        self.name = eventName
        self.des = eventDes
        self.time = eventTime
        self.userID = user
        self.level = importance
        self.date = date

    def __str__(self):
        x = dict()
        x['name'] = self.name
        x['time'] = self.time
        x['User'] = self.userID
        x['Importance'] = self.level
        x['date'] = self.date
        x['description'] = self.des
        return str(x)

    def timeToSeconds(self):
        x = self.time.split(':')
        return x[0] * 3600 + x[1] * 60
