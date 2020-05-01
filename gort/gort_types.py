# Data given in constraint JSON

# Instrument name
#   * string
# Minimum book level
#   * int
# Maximum book level
#   * int
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

# Class name
#   * string
# Class ID
#   * int
# Required class
#   * boolean
# Book based
#   * boolean
# Minimum book level
#   * int
# Maximum book level
#   * int
# Age based
#   * boolean
# Minimum age
#   * int
# Maximum age
#   * int
# Instrument based
#   * boolean
# Instrument list
#   * list(string)
# Room size
#   * int
#   * small = 1
#   * medium = 2
#   * large = 3
# Enrollment max
#   * int
# Needs accompanist
#   * boolean
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
            + ('\n'.join(self.students) if self.students else '\t\tNone')
        )

    # TODO
    # Set the instructor for the class
    def set_instructor (self, instructor):
        pass

    # TODO
    # Add a student to the list of students
    def add_student (self, student):
        pass

# Instructor name
#   * string
# Instructor ID
#   * int
# List of instruments
#   * list(string)
# List of teachable classes
#   * list((class id, minimmum level, maximum level))
#   ** class id: int
#   ** minimum level: int
#   ** maximum level: int
# Slots available for
#   * list(int)
# Maximum slots available for
#   * int
class Instructor:
    def __init__ (self, name, id_, instruments, can_teach, avail, max_slots):
        self.name = name
        self.id = id_
        self.instruments = instruments
        self.can_teach = [
            (x['id'], x['bookLevelMin'], x['bookLevelMax'])
            for x in can_teach
        ]
        self.avail = avail
        self.max_slots = max_slots

    def __str__ (self):
        return (
            f'{self.name} ({self.id}):\n'
            f'\tInstruments: '
            + (' '.join(self.instruments)) + '\n'
            + f'\tCan teach:\n'
            + ('\n'.join([
                  f'\t\tID: {x[0]}\n'
                  f'\t\tMinimum level: {x[1]}\n'
                  f'\t\tMaximum level: {x[2]}'
                  for x in self.can_teach
              ]) + '\n')
            + f'\tSlots available: '
            + (' '.join([str(x) for x in self.avail]) + '\n')
            + f'\tMaximum slots: {self.max_slots}'
        )

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
