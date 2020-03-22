class Nurse:

  def __init__(self, lastShift, doneShifts):
    self._lastShift = lastShift
    self._doneShifts = doneShifts 
  
  def getDone(self):
    return self._doneShifts


class WeekDay():
  def __init__(self, requiredShifts, day, afternoon, night):
    self._day = day
    self._afternoon = afternoon
    self._night = night

def insertion_sort(nurses):

    for i in range(len(nurses)):
        cursor = nurses[i]
        pos = i
        
        while pos > 0 and nurses[pos - 1].getDone() > cursor.getDone():
            # Swap the number down the list
            nurses[pos] = nurses[pos - 1]
            pos = pos - 1
        # Break and do the final swap
        nurses[pos] = cursor

    return nurses

def 


def main():
  allNurses = []
  week = []
  count = 0
  while(count < 15):
    allNurses.append(Nurse(0, 0))
    count += 1
  count = 0
  while(count < 7):
    if (count == 2 or count == 5 or count == 6):
      week.append(WeekDay([], [], []))
    else:
      week.append(WeekDay([], [], []))
    count += 1
