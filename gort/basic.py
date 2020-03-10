from __future__ import print_function
from ortools.sat.python import cp_model

def main():
    # Data.
    num_teachers = 3
    num_slots = 3
    num_kids = 10
    class_size = 4
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

   	#each student must have 1 teacher at each slot
    for s in all_slots:
    	for k in all_kids:
    		model.Add(sum(slots[(t,s,k)] for t in all_teachers) == 1)

    #There can be a max of 5 students in a class
    for s in all_slots:
    	for t in all_teachers:
    		model.Add(sum(slots[(t,s,k)] for k in all_kids) <= class_size)


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
    
    #Statistics


if __name__ == '__main__':
    main()