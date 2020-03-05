import re

# Data format in CSV
# First Name (student)
#   * string
# Last Name (student)
#   * string
# Age (student)
#   * int
# Last Name (instructor)
#   * string
# Instrument
#   * string
# Book
#   * string
# Violin Book 1 Piece
#   * string
#   * possibly empty
# Orchestra Participation
#   * boolean
# Enroll in Chamber
#   * boolean
#   * possibly empty
# Music and Movement
#   * int
# Art
#   * int
# Fiddling (violin/viola)
#   * int
# Fiddling (cello)
#   * int
# Improv
#   * int
# Compose and Compute
#   * int
# Musicianship
#   * int
# Dalcroze
#   * int

class CSVData:
    def __init__ (self, fname, lname, age, instructor, inst, book, book1, orch,
        chamber, mu_mvmt, art, fid_vi, fid_ce, improv, com_com, mus, dal):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.instructor = instructor
        self.inst = inst
        self.book = book
        self.book1 = book1
        self.orch = orch
        self.chamber = chamber
        self.mu_mvmt = mu_mvmt
        self.art = art
        self.fid_vi = fid_vi
        self.fid_ce = fid_ce
        self.improv = improv
        self.com_com = com_com
        self.mus = mus
        self.dal = dal

    def __str__ (self):
        return (
            f'{self.fname} {self.lname}:\n'
            f'\tAge: {self.age}\n'
            f'\tInstructor: {self.instructor}\n'
            f'\tInstrument: {self.inst}\n'
            f'\tBook: {self.book}\n'
            f'\tBook 1 piece: {self.book1 if self.book1 else "n/a"}\n'
            f'\tParticipating in orchestra: {"Yes" if self.orch else "No"}\n'
            f'\tEnroll in chamber: {"Yes" if self.chamber else "No"}\n'
            f'\tMusic & Movement: {self.mu_mvmt}\n'
            f'\tArt: {self.art}\n'
            f'\tFiddling (Violin/Viola): {self.fid_vi}\n'
            f'\tFiddling (Cello): {self.fid_ce}\n'
            f'\tImprovisation: {self.improv}\n'
            f'\tCompose and Compute: {self.com_com}\n'
            f'\tMusicianship: {self.mus}\n'
            f'\tDalcroze: {self.dal}'
        )

# Import the data from a CVS file given as a text-mode file-like object
def import_csv(csv):
    ret = []
    # Skip the first line which is just the fields
    next(csv)
    # Go through the CSV file line by line
    for line in csv:
        # Replace "yes" strings with T
        line = re.sub('"yes,.*?"', 'T', line, flags=re.IGNORECASE)
        # Replace "no" strings with F
        line = re.sub('"no,.*?"', 'F', line, flags=re.IGNORECASE)
        # Split into individual bits
        spl = line.split(',')
        # Convert into numbers
        spl = [int(x) if x.isdigit() else x for x in spl]
        # Convert True/False
        spl = [True if x == 'T'
            else False if x == 'F'
            else x
            for x in spl]
        # Convert empty string
        spl = [None if x == '' else x for x in spl]
        ret.append(CSVData(*spl))

    return ret
