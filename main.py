import search.py


class Shift:
    def __init__(self, weekDay, nrNursesReq, time):
        self.weekDay = weekDay
        self.nrNursesReq = nrNursesReq
        self.dictOfNurses = {}
        self.NrNurses = 0
        self.time = time

    def addNurse(self, Nurse):
        if Nurse.ID in self.dictOfNurses:
            print("Nurse is already in this shift! Try another one")
            return -1
        else:
            self.dictOfNurses["Nurse.ID"] = Nurse
            self.NrNurses = self.NrofNurses + 1
            print("Added nurse" + Nurse.ID + "to" + self.time + "Shift in day" + self.weekDay.day + "\n")
            return 1

class Nurse:
    def __init__(self, NurseID):
        self.ID = NurseID
        self.shiftList = []
    def addshift(self, Shift):
        if Shift not in self.shiftList:
            self.shiftList.append(Shift)
            return 1
        else:
            print("Nurse already had that shift")
            return -1

class ScheduleP(search.Problem):
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, Nurses, Shifts):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.Shifts = Shifts
        self.Nurses = Nurses
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

def BuildClass():
    nList = []
    sList = []
    for i in range(0, 15):
        nList.append(Nurse(i))
    for i in range(1,8):
        if i == 1 or 2 or 4 or 5:
            sList.append(Shift(i, 9, "Morning"))
            sList.append(Shift(i, 6, "Afternoon"))
            sList.append(Shift(i, 5, "Night"))
        if i == 3 or 6 or 7:
            sList.append(Shift(i, 6, "Morning"))
            sList.append(Shift(i, 6, "Afternoon"))
            sList.append(Shift(i, 5, "Night"))

