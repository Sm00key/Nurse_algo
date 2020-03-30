import search
import copy


class state_t:
    def __init__(self, nurses, shifts):
        self.nurses = nurses
        self.shifts = {}
        self.cost = 0

        for shift in shifts:
            self.shifts[shift.nr] = shift

    def __lt__(self, node_t):
        return self.cost < node_t.cost


class Shift:
    def __init__(self, number, nrNursesReq, time, pshift):
        self.nr = number
        self.nrNursesReq = nrNursesReq
        self.dictOfNurses = {}
        self.NrNurses = 0
        self.time = time
        self.prevshift = pshift

    def addNurse(self, Nurse):
        if Nurse.ID in self.dictOfNurses:
            print("Nurse is already in this shift! Try another one")
            return -1
        else:
            self.dictOfNurses[Nurse.ID] = Nurse
            self.NrNurses = self.NrNurses + 1
            # print("Added nurse" + Nurse.ID + "to" + self.time + "Shift in day" + self.weekDay.day + "\n")
            return 1


class Nurse:
    def __init__(self, NurseID):
        self.ID = NurseID
        self.shiftList = []

    def addShift(self, Shift):
        if Shift not in self.shiftList:
            self.shiftList.append(Shift)
            return 1
        else:
            print("Nurse already has that shift")
            return -1

    def getShiftList(self):
        return self.shiftList


class ScheduleP(search.Problem):
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, nlist, slist):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = state_t(None, slist)
        super().__init__(self.initial)
        self.shifts = slist
        self.nurses = nlist

    def actions(self, state):
        actions = []
        for shift in state.shifts.values():
            if shift.NrNurses < shift.nrNursesReq:
                for nurse in self.nurses:
                    if nurse.ID not in shift.dictOfNurses:
                        if (shift.prevshift is None) or (len(shift.prevshift.dictOfNurses) == 0):
                            actions.append((nurse, shift))
                        elif nurse.ID not in shift.prevshift.dictOfNurses: #POTENTIAL BUG
                            actions.append((nurse, shift))
                        elif shift.prevshift.prevshift is None:
                            actions.append((nurse, shift))
                        elif nurse.ID not in shift.prevshift.prevshift.dictOfNurses:
                            actions.append((nurse, shift))
                break
        return actions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_state = copy.deepcopy(state)
        new_state.shifts[action[1].nr].addNurse(action[0])
        new_state.cost += self.path_cost(0, state, action, new_state)
        return new_state

    def goal_test(self, state):

        """Return True if the sta-te is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        # If in all shifts the number of nurses is equal to the number of nurses 
        # required then all shifts have been successfully attributed
        goal = True
        for shift in state.shifts.values():
            if shift.NrNurses != shift.nrNursesReq:
                goal = False
                break
        return goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        cost: int = 0
        if state2.shifts[action[1].nr].prevshift is None:
            return 0
        if action[0].ID in state2.shifts[action[1].nr].prevshift.dictOfNurses.keys():
            cost = 1

        return cost

    def value(self, state):
        """For optimization problems, each state has a value. Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

    def h(self, n):
        return 0


def BuildClass():
    nList = []
    sList = []
    s1, s2, s3 = None, None, None
    id = 0
    for i in range(0, 15):
        nList.append(Nurse(i))
    for i in list(range(1, 8)):
        if i == 1:
            s1 = Shift(id, 9, "Morning", None)
            id += 1
            s2 = Shift(id, 6, "Afternoon", s1)
            id += 1
            s3 = Shift(id, 5, "Night", s2)
            id += 1
        if i == 2 or i == 4 or i == 5:
            s1 = Shift(id, 9, "Morning", s3)
            id += 1
            s2 = Shift(id, 6, "Afternoon", s1)
            id += 1
            s3 = Shift(id, 5, "Night", s2)
            id += 1
        if i == 3 or i == 6 or i == 7:
            s1 = Shift(id, 6, "Morning", s3)
            id += 1
            s2 = Shift(id, 6, "Afternoon", s1)
            id += 1
            s3 = Shift(id, 5, "Night", s2)
            id += 1
        sList.append(s1)
        sList.append(s2)
        sList.append(s3)
    return nList, sList


nlist_t, slist_t = BuildClass()
Pb = ScheduleP(nlist_t, slist_t)  # INITIAL STATE

node = search.astar_search(Pb)
for shift in node.state.shifts.values():
    print("Shift nr: " + str(shift.nr) + "  with the following nurses:")
    for nurse in shift.dictOfNurses.values():
        print(nurse.ID, end="\t")
    print()

