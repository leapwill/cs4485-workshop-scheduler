from __future__ import print_function
import random
from ortools.sat.python import cp_model

def main():
    # Data.
    num_teachers = 3
    num_slots = 3
    num_kids = 10
    class_size = 4
    num_of_classes = 4
    count = 0;
    all_teachers = range(num_teachers)
    all_slots = range(num_slots)
    all_kids = range(num_kids)
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # teacher[c][s]: teacher 't' of student k in slot s
    teachers = {}
    for k in all_kids:
        for s in all_slots:
            teachers[(k, s
                )] = model.NewIntVar(0, num_of_teachers - 1, 'teacher')

    # Creates shift variables.
    # classType[(s, t)]: teacher 't' during time slot 's' is teaching which class.
    # class type 0 is no class/free
    # class type 1 is master class, 2 is group
    # 3 is chamber, 4 is elective
    classType = {}
    #classType = model.NewIntVar(0, num_of_classes - 1, 'classType')
    for t in all_teachers:
        for s in all_slots:
                suffix = '_%i_%i' % (s, t)
                classType[(t, s
                    )] = model.NewIntVar(0, num_of_classes - 1, 'classType')


   	#1. For every child k and required class d, k is assigned d in exactly one slot.
    #Required classes are Masterclass and group class or 0 and 1
    #class type0 [t][s] == teacher[t] [k][s]
    for k in all_kids:
        for s in all_slots:
            for t in all_teachers:
                #find [t][s] for class type 0
                ##classType[(k,s)] = [t]

    #2. For every teacher t and slot s, t can teach the class that t is assigned to teach in slot s.
    for t in all_teachers:
        for s in all_slots:
            if teacher.canTeach classType:
                model.Add(teachers[(k,s)] = k.classTally)


    #3. For every child k and slot s, the teacher assigned to teach k in s is competent in k’s instrument.
    for k in all_kids:
        for t in all_teachers:
            if t is competent in ks instrument:
                model.Add((teachers[(k,s)] for s in all_slots) = t)
    

    #4. For every teacher t, the number of slots during which t is assigned to teach is bounded by t’s preference.
    # Does this refer to the number of classes the teacher wants to teach?
    # Does this refer to the classes the teacher wants to teach? like art etc.
    for t in all_teachers:
        model.Add(sum(teachers[(k,s)] for s in all_slots) >= t.preference)

    #5.  For every teacher t, t is not assigned to teac
    +
        for s in all_slots:
            #if teacher is not availabe:
                #model.Add(classType[(t,s)] = 0)

    #6. For every child k, the total number of classes (including electives) assigned to k is the equal to k’s class tally.
    model.Add(sum(teachers[(k,s)] for k in all_kids) = k.classTally)


    #7. All classes assigned to a young child are in the morning.
    for k in all_kids:
        #if kid is young kid
            #teacher = null in slot 3, 4, 5


    #Creates the solver and solve
    solver = cp_model.CpSolver()
    solver.Solve(model)

    for s in all_slots:
    	print ('Slot', s)
        for k in all_kids:
    		if solver.Value(slots[(k,s)]) == 1:
    			print('Teacher ',  solver.Value(classType[(k,s)]), ' student ', k)
    	print()

    for s in all_slots:
        print ('Slot', s)
        for t in all_teachers:
            print('Teacher ', t, ' class ', solver.Value(classType[(t,s)]))
        print()


if __name__ == '__main__':
    main()