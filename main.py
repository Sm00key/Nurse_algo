import search
import copy


class state_t:
    def __init__(self, nurses, shifts):
        self.nurses = nurses
        self.shifts = {}
        self.cost = 0

        for shift in shifts:
            self.shifts[shift.nr] = shift


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
        self.shifts = nlist
        self.nurses = slist

    def actions(self, state):
        actions = []
        for shift in state.shifts:
            if shift.NrNurses < shift.nrNursesReq:
                for nurse in self.nurses:
                    if nurse.ID not in shift.dictOfNurses:
                        if shift.prevshift is None:
                            actions.append((nurse, shift))
                        elif shift.prevshift.dictOfNurses[nurse.ID] is not shift.prevshift.prevshift.dictOfNurses[
                            nurse.ID]:
                            actions.append((nurse, shift))

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_state = copy.deepcopy(state)
        new_state.shifts[action[1].nr].addNurse(action[1])

    def goal_test(self, state):

        """Return True if the sta-te is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        # If in all shifts the number of nurses is equal to the number of nurses 
        # required then all shifts have been successfully attributed
        goal = True
        for shift in state.shifts:
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
        cost = 0
        flag = False

        if action[0].ID in state2.shifts[action[1]].prevshift.dictOfNurse.keys():
            cost = 1

        return c + cost

    def value(self, state):
        """For optimization problems, each state has a value. Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


def BuildClass():
    nList = []
    sList = []
    s1, s2, s3 = None, None, None
    for i in range(0, 15):
        nList.append(Nurse(i))
    for i in range(1, 8):
        if i == 1:
            s1 = Shift(i + 1, 9, "Morning", None)
            s2 = Shift(i + 2, 6, "Afternoon", s1)
            s3 = Shift(i + 3, 5, "Night", s2)
        if i == 2 or 4 or 5:
            s1 = Shift(i + 1, 9, "Morning", s3)
            s2 = Shift(i + 2, 6, "Afternoon", s1)
            s3 = Shift(i + 3, 5, "Night", s2)
        if i == 3 or 6 or 7:
            s1 = Shift(i + 1, 6, "Morning", s3)
            s2 = Shift(i + 2, 6, "Afternoon", s1)
            s2 = Shift(i + 3, 5, "Night", s2)
        sList.append(s1)
        sList.append(s2)
        sList.append(s3)
    return nList, sList


nlist, slist = BuildClass()
Pb = ScheduleP(nlist, slist)  # INITIAL STATE

node = search.astar_search(Pb, None)