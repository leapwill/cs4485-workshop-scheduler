from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model

class instClass:
    ClassID = 0
    ClassType = 0
    Instrument = 0
    MaxSize = 0
    Instructor = 0
    Students = []

    def __init__(self, classIdCounter, classType, instrument, maxSize):
        #intializes previous variables.
        self.ClassID = classIdCounter
        self.ClassType = classType
        self.Instrument = instrument
        self.MaxSize = maxSize

    def setInstructor(self, instr):
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

    def __init__(self, full,last,first,ag,inst,bl, pteach):#, prefTeach, a number, another number in brackets, array
        self.fullName = full
        self.firstName = first
        self.lastName = last
        self.age = ag
        self.instrument = inst
        self.bookLevel = bl
        self.prefTeach = pteach

    def setMasterClass(self, ID):
        self.masterClassId = ID

class Teacher:
    fullName = ""
    agePref = 0
    classPref = 0
    instrument = 0
    #timeAvai = 0
    booksCertfied = []
    classesCertified = []

    def __init__(self, full,age,cpref,inst,bcert,ccert):
        self.fullName = full
        self.agePref = age
        self.classPref = cpref
        self.instrument = inst
        self.booksCertfied = bcert
        self.classesCertified = ccert

def sortAgeArray(Array):
    arrayToSort = Array;
    if(len(arrayToSort) <=0):
        return arrayToSort
    placeHolder = arrayToSort[0];
    goAgain = True;

    while(goAgain):
        goAgain = False;
        for i in range(len(arrayToSort)-1):
            if arrayToSort[i+1].age < arrayToSort[i].age:
                placeHolder = arrayToSort[i+1]
                arrayToSort[i+1] = arrayToSort[i]
                arrayToSort[i] = placeHolder;
                goAgain = True;

    return arrayToSort


def SimpleSatProgram():
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    StudentBody = []
    for i in range(5):
        StudentBody.append(Student("Jimmy Neutron"+str(i), "Neutron", "Jimmy", 13, 1, 3, "Timmy"))

    for i in range(6):
        StudentBody.append(Student("Timmy Turner"+str(i), "Turner", "Timmy", 10, 0, 1, "Crocker"))

    for i in range(3):
        StudentBody.append(Student("Phineas Flynn"+str(i), "Flynn", "Phineas", 12, 4, 5, "Candace"))

    for i in range(4):
        StudentBody.append(Student("Ferb Flynn"+str(i), "Flynn", "Ferb", 11, 4, 5, "Candace"))

    for i in range(10):
        StudentBody.append(Student("Kim Possible"+str(i), "Possible", "Kim", 16, 0, 4, "Molerat"))

    for i in range(3):
        StudentBody.append(Student("Ron Stoppable"+str(i), "Stoppable", "Ron", 16, 0, 2, "Molerat"))


    BL1Students = []
    BL2Students = []
    BL3Students = []
    BL4Students = []
    BL5Students = []

    
    for i in range(5):
        for s in StudentBody:
            if(s.instrument == i):
                if(s.bookLevel == 1):
                    BL1Students.append(s);
                if(s.bookLevel == 2):
                    BL2Students.append(s);
                if(s.bookLevel == 3):
                    BL3Students.append(s);
                if(s.bookLevel == 4):
                    BL4Students.append(s);
                if(s.bookLevel == 5):
                    BL5Students.append(s);
        BL1Students = sortAgeArray(BL1Students);
        BL2Students = sortAgeArray(BL2Students);
        BL3Students = sortAgeArray(BL3Students);
        BL4Students = sortAgeArray(BL4Students);
        BL5Students = sortAgeArray(BL5Students);

        print("INSTRUMENT " + str(i))
        print();

        print("BL1 STUDENTS")
        for s in BL1Students:
            print(s.fullName)
        print("BL2 STUDENTS")
        for s in BL2Students:
            print(s.fullName)
        print("BL3 STUDENTS")
        for s in BL3Students:
            print(s.fullName)
        print("BL4 STUDENTS")
        for s in BL4Students:
            print(s.fullName)
        print("BL5 STUDENTS")
        for s in BL5Students:
            print(s.fullName);

        BL1Students.clear();
        BL2Students.clear();
        BL3Students.clear();
        BL4Students.clear();
        BL5Students.clear();
        print();






    # model = cp_model.CpModel()

    # # Creates the variables.
    # num_vals = 3
    # x = model.NewIntVar(0, num_vals - 1, 'x')
    # y = model.NewIntVar(0, num_vals - 1, 'y')
    # z = model.NewIntVar(0, num_vals - 1, 'z')

    # # Creates the constraints.
    # model.Add(x != y)

    # # Creates a solver and solves the model.
    # solver = cp_model.CpSolver()
    # status = solver.Solve(model)

    # if status == cp_model.FEASIBLE:
    #     print('x = %i' % solver.Value(x))
    #     print('y = %i' % solver.Value(y))
    #     print('z = %i' % solver.Value(z))


SimpleSatProgram()