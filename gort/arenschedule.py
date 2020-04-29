from __future__ import print_function
from ortools.sat.python import cp_model


def main():
    # Data.
    num_teachers = 23
    num_slots = 3
    num_kids = 23
    num_types = 6
    class_size = 7
    class_types = 10 #perday?
    num_instruments = 5
    all_classes = range(class_types)
    all_teachers = range(num_teachers)
    all_slots = range(num_slots)
    all_kids = range(num_kids)
    all_instruments = range(num_instruments)
    all_types = range
    # Creates the model.
    model = cp_model.CpModel()

    
    classAttendance = {}
    teacherAttendance = {}
    childInfo = [ #inum, instrument
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 1),
        (5, 1),
        (6, 1),
        (7, 1),
        (8, 2),
        (9, 2),
        (10, 2),
        (11, 2),
        (12, 3),
        (13, 3),
        (14, 3),
        (15, 3),
        (16, 4),
        (17, 4),
        (18, 4),
        (19, 1),
        (20, 2),
        (21, 3),
        (22, 4),
    ]
    slotInfo = [
        (0, "8:00"),
        (1, "9:30"),
        (2, "11:00"),
        (3, "12:30"),
        (4, "2:00"),

    ]
    teacherInfo = [
        #number, instrument, limit (-1 is no limit)
        (0, 0, 1),
        (1, 3, -1),
        (2, 4, -1),
        (3, 1, -1),
        (4, 2, -1),
        (5, 0, 1),
        (6, 3, -1),
        (7, 4, -1),
        (8, 1, -1),
        (9, 0, -1),
        (10, 2, -1),
        (11, 0, -1),
        (12, 0, -1),
        (13, 3, -1),
        (14, 4, -1),
        (15, 1, -1),
        (16, 2, -1),
        (17, 0, -1),
        (18, 0, -1),
        (19, 3, -1),
        (20, 4, -1),
        (21, 1, -1),
        (22, 2, -1),
        (23, 0, -1)
    ]
    classInfo = [
        (0, 0, 0),#number, instrument, classType (master, group)}
        (1, 1, 0),
        (2, 2, 0),
        (3, 3, 0),
        (4, 4, 0),
        (5, 0, 1),
        (6, 1, 1),
        (7, 2, 1),
        (8, 3, 1),
        (9, 4, 1)
    ]

    teacherAvailabilityConstraints = [
        #teacher, slot unable
        (0, 0) #teacher 0 will not work mornings
    ]

    teacherLimit = [
        (0, 1)#teacher 0 will only teach 1 class
    ]

    #Teach constraints

    for t in all_teachers:
        for c in all_classes:
            for s in all_slots:
                teacherAttendance[t, c, s] = model.NewBoolVar('teacherAttendance%i_%i_%i' % (t, c, s))

    #One Teacher Per Class
    for s in all_slots:
        for c in all_classes:
            model.Add(sum(teacherAttendance[t,c,s] for t in all_teachers) == 1)

    # No more than 1 teacher per class, teachers can not be assigned
    for t in all_teachers:
        for s in all_slots:
            model.Add(sum(teacherAttendance[t,c,s] for c in all_classes) <= 1)

    #a requested off-slot
    for t in all_teachers:
        for s in all_slots:
            for c in all_classes:
                if t < len(teacherAvailabilityConstraints):
                    if teacherAvailabilityConstraints[t][1] == s:
                        model.Add(teacherAttendance[t,c,s] == 0)

    #teacher limits
    for t in all_teachers:
        for c in all_classes:
            if teacherInfo[t][2] > 0:
                model.Add(sum(teacherAttendance[t,c,s] for s in all_slots) <= teacherInfo[t][2])

    #Teachers only teach classes for instruments they are proficient at
    for s in all_slots:
        for c in all_classes:
            for t in all_teachers:
                model.Add( teacherInfo[t][1] == classInfo[c][1] ).OnlyEnforceIf(teacherAttendance[t,c,s])

    #Kid constraints
    for k in all_kids:
        for c in all_classes:
            for s in all_slots:
                classAttendance[k, c, s] = model.NewBoolVar('classAttendance%i_%i_%i' % (k, c, s))


    #One Class per time slot
    for k in all_kids:
        for s in all_slots:
            model.Add(sum(classAttendance[k, c, s] for c in all_classes) == 1)

    #Students only go to classes for their own instruments.
    for k in all_kids:
        for s in all_slots:
            for c in all_classes:
                model.Add( childInfo[k][1] == classInfo[c][1]).OnlyEnforceIf(classAttendance[k,c,s])

    # Max size and minSize
    for s in all_slots:
        for c in all_classes:
            model.Add(sum(classAttendance[k,c,s] for k in all_kids) <= class_size)
    #Minumum class size
    #for s in all_slots:
    #    for c in all_classes:
    #        model.Add(sum(classAttendance[k,c,s] for k in all_kids) > 0)

    solver = cp_model.CpSolver()
    solver.Solve(model)

    for s in all_slots:
        print("")
        print("Slot", s, ", Time: ", slotInfo[s][1])
        for c in all_classes:
            print("Class", c, " Instrument: ", classInfo[c][1], " Type: ", classInfo[c][2])
            for t in all_teachers:
                if solver.Value(teacherAttendance[(t,c,s)]) == 1:
                    print("Taught by Teacher ", t, ", Who is proficient in: Instrument ", teacherInfo[t][1])
            for k in all_kids:
                if solver.Value(classAttendance[(k,c,s)]) == 1:
                    print("Kid ", k, "is here. (Plays ", childInfo[k][1], ")")

    #model.AddAllowedAssignments('')

if __name__ == '__main__':
    main()