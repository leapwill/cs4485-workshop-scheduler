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
    # slots[(t, s, c)]: teacher 't' during time slot 's' with every student 's'.
    slots = {}
    for t in all_teachers:
        for s in all_slots:
            for k in all_kids:
                slots[(t, s,
                    k)] = model.NewBoolVar('slots_t%is%ik%i' % (t, s, k))

    # Creates shift variables.
    # classType[(t, s)]: teacher 't' during time slot 's' is teaching which class.
    # class type 0 is master class, 1 is group, 2 is chamber, 3 is elective
    classType = {}
    #classType = model.NewIntVar(0, num_of_classes - 1, 'classType')
    for t in all_teachers:
        for s in all_slots:
                suffix = '_%i_%i' % (s, t)
                classType[(t, s
                    )] = model.NewIntVar(0, num_of_classes - 1, 'classType')


   	#each student must have 1 teacher at each slot
    for s in all_slots:
    	for k in all_kids:
    		model.Add(sum(slots[(t,s,k)] for t in all_teachers) == 1)

    #There can be a max of 5 students in a class
    for s in all_slots:
    	for t in all_teachers:
    		model.Add(sum(slots[(t,s,k)] for k in all_kids) <= class_size)

    for s in all_slots:
        for t in all_teachers:
            #class type is count mod num_of_classes
            model.AddModuloEquality(classType[(t,s)], count, num_of_classes)
            count += 1
            #random class type
            #classType[(t,s)] = random.randrange(0, num_of_classes)

    #Creates the solver and solve
    solver = cp_model.CpSolver()
    solver.Solve(model)
    for s in all_slots:
    	print ('Slot', s)
    	for t in all_teachers:
    		print()
    		for k in all_kids:
    			if solver.Value(slots[(t,s,k)]) == 1:
    				print('Teacher ', t, ' student ', k)
    	print()

    for s in all_slots:
        print ('Slot', s)
        for t in all_teachers:
            print('Teacher ', t, ' class ', solver.Value(classType[(t,s)]))
        print()

    
    #Statistics


if __name__ == '__main__':
    main()