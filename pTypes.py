import pyttsx3
import classes as c

# Config
programName = ''
agentVoice = pyttsx3.init()
agentVoice.setProperty('rate', 130)
agentGender = ''


cameraOn = False

# Product Information
version = '0.5'
creator = 'Mohamed Mostafa'
email = 'mohamed.01061@gmail.com'

# Helpers
creatingProfile = False

talking = False

eventListChanged = False   # tells the thread to optimize the list in the next cycle

configKeys = ['pName', 'pGender', 'Camera']

eventList = list()

# Speeches
finishSettings = ["That's all", "All is set now", "Everything is greet now", "That will be all", "I think we have "
                                                                                                 "finished"]

agentAge = ['I think i have been born today', 'May be days or even years', 'Ooh my age i really don\'t remember it',
            'I don\'t know if i have one', 'hmm should i have age\ni mean i am an agent']

youAreKidding = ["Sure you are kidding", "ha ha ha ha ha it must be a joke", "impossible please stop joking",
                 "Don't be ridiculous"
    , "Good joke"]

error = ["Something went wrong", "I don't know\nbut something happened uncorrectly", "Maybe something missed"
    , "I had an error", "Why all programs has errors", "Broken"]

welcome = ['Hola', 'Hi', "Hello", "Welcome", "Hlaa", "Bonjour", "How are you", "Bienvenidos", "Yōkoso", "Chao",
           "ahlan", "Greetings"]

needing = ['I need {x}', '{x} is important to me', 'you have to tell me {x}', 'it seems you have not told me about {x}']

exiting = ['See you soon', "Don't be late", "See you later", "Sure", "Happy to be useful for a short time",
           "Auf Wiedersehen"
    , "hasta luego", "Ciao", "ela aliqaa ya", "Au revoir", "Sayuōnara"]

dailyEventStored = ["I have just stored {x} as a daily event", "{x} is a daily event now", "{x} became a daily event",
                    "Done storing {x} as a daily event"]

weeklyEventStored = ["I have just stored {x} as a weekly event", "{x} is a weekly event now",
                     "{x} became a weekly event", "Done storing {x} as a weekly event", "I hope it is a great week "
                                                                                        "for {x}"]

monthlyEventStored = ["I have just stored {x} as a monthly event", "{x} is a monthly event now",
                      "{x} became a monthly event", "Done storing {x} as a monthly event", "I hope it is a great month "
                                                                                           "for {x}"]

yearlyEventStored = ["I have just stored {x} as a yearly event", "{x} is a yearly event now",
                     "{x} became a yearly event", "Done storing {x} as a yearly event", "I hope it is a great year "
                                                                                        "for {x}"]

customEventStored = ["I have just stored {x} as a only once event", "{x} is a only once event now",
                     "{x} became a only once event", "Done storing {x} as a only once event"]

eventAfterTime = ["I think you should know that {x} starts after {y}","Remember,{x} is about to start after {y}"
                  ,"Please be aware about {x} which will begin after {y}",
                  "Attention please,It is just {y} before {x} begins",
                  "I think you should finish what yoy are doing quickly\n{x} is going to start after {y}",
                  "Tin tin tin,{x} is going to start after {y}","It is only {y} for {x}","Hey,{y} for {x}",
                  "You shouldn't miss {x} after {y} from now","Time time time time time,{x} will begin in just {y}",
                  "Do you know that {x} will begin in only {y}"]

hopeBest = ["I hope the best for you","Be careful","Get ready my little bird","You can do it","Work hard",
            "Best wishes for you my dear"]

criticalEventTomorrow = ["You should know that {x} will be tomorrow","Tomorrow is the day for {x} be ready",
                         "Finally tomorrow is the day for {x}"]

currentProfile = 0

dailyEvents = list()
weeklyEvents = list()
monthlyEvents = list()
yearlyEvents = list()
customEvents = list()


# Packages
maxProfileNumber = 2