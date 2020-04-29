class Instrument:
    def __init__ (self, name, min_, max_):
        self.name = name
        self.min = min_
        self.max = max_

    def __str__ (self):
        return (
            f'{self.name}:\n'
            f'\tMinimum level: {self.min}\n'
            f'\tMaximum level: {self.max}'
        )

class Class:
    def __init__ (self, name, id_, required, book_based, min_book, max_book,
                  age_based, min_age, max_age, instrument_based, instruments,
                  size, max_enroll, need_accompanist):
        self.name = name
        self.id = id_
        self.required = required
        self.book_based = book_based
        self.min_book = min_book
        self.max_book = max_book
        self.age_based = age_based
        self.min_age = min_age
        self.max_age = max_age
        self.instrument_based = instrument_based
        self.instruments = instruments
        self.size = size
        self.max_enroll = max_enroll
        self.need_accompanist = need_accompanist
        # Initialize with no instructor or students
        self.instructor = 0
        self.students = []

    def __str__ (self):
        return (
            f'{self.name} ({self.id}):\n'
            f'\tInstructor: '
            + (f'{self.instructor}\n' if self.instructor else 'None\n')
            + f'\tRequired: '
            + ('Yes\n' if self.required else 'No\n')
            + f'\tBook based: '
            + ('Yes\n' if self.book_based else 'No\n')
            + (f'\t\tMinimum level: {self.min_book}\n'
               if self.book_based else '')
            + (f'\t\tMaximum level: {self.max_book}\n'
               if self.book_based else '')
            + f'\tAge based: '
            + ('Yes\n' if self.age_based else 'No\n')
            + (f'\t\tMinimum age: {self.min_age}\n'
               if self.age_based else '')
            + (f'\t\tMaximum age: {self.max_age}\n'
               if self.age_based else '')
            + f'\tInstrument based: '
            + ('Yes\n' if self.instrument_based else 'No\n')
            + ('\tInstruments: ' if self.instrument_based else '')
            + (' '.join(self.instruments) + '\n'
               if self.instrument_based else '')
            + f'\tRoom size: '
            + ('Small\n' if self.size == 1
               else 'Medium\n' if self.size == 2
               else 'Large\n')
            + f'\tMax students: {self.max_enroll}\n'
            f'\tNeeds accompanist: '
            + ('Yes\n' if self.need_accompanist else 'No\n')
            + f'\tStudents:\n'
            + ('\n'.join(self.students) if self.students else '\t\tNone\n')
        )

    # TODO
    # Set the instructor for the class
    def set_instructor (self, instructor):
        pass

    # TODO
    # Add a student to the list of students
    def add_student (self, student):
        pass

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
