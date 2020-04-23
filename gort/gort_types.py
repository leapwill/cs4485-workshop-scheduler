class instClass:
    ClassID = 0
    ClassType = 0
    Instrument = 0
    MaxSize = 0
    Instructor = 0
    Students = []

    def __init__ (self, classIdCounter, classType, instrument, maxSize):
        #intializes previous variables.
        self.ClassID = classIdCounter
        self.ClassType = classType
        self.Instrument = instrument
        self.MaxSize = maxSize

    def setInstructor (self, instr):
        self.Instructor = instr

class Student:
    fullName = ""
    firstName = ""
    lastName = ""
    age = 0
    instrument = 0
    bookLevel = 0
    masterClassId = 0
    prefTeach = 0

    def __init__ (self, full,last,first,ag,inst,bl, pteach):#, prefTeach, a number, another number in brackets, array
        self.fullName = full
        self.firstName = first
        self.lastName = last
        self.age = ag
        self.instrument = inst
        self.bookLevel = bl
        self.prefTeach = pteach

    def __str__ (self):
        return (
            f'{self.fullName}:\n'
            f'\tAge: {self.age}\n'
            f'\tInstrument: {self.instrument}\n'
            '\tLevel: '
            + (f'{self.bookLevel}\n' if self.bookLevel > 0 else 'Pre-Twinkle\n')
            + f'\tMasterclass: {self.masterClassId}\n'
            f'\tPreferred Teacher: {self.prefTeach}'
        )

    def setMasterClass (self, ID):
        self.masterClassId = ID

class Teacher:
    fullName = ""
    agePref = 0
    classPref = 0
    instrument = 0
    #timeAvai = 0
    booksCertfied = []
    classesCertified = []

    def __init__ (self, full,age,cpref,inst,bcert,ccert):
        self.fullName = full
        self.agePref = age
        self.classPref = cpref
        self.instrument = inst
        self.booksCertfied = bcert
        self.classesCertified = ccert
