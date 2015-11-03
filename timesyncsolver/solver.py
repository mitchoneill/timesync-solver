import Numberjack as Nj


class Teachers(object):
    """Will be expanded to allow constraints for individual teachers"""
    def __init__(self):
        self.store = list()

    def add(self, teachers):
        if isinstance(teachers, (list, tuple)):
            self.store.extend(teachers)
        elif isinstance(teachers, str):
            self.store.append(teachers)
        else:
            raise TypeError('only lists, tuples and strings '
                            'of teachers can be added')


class Subjects(object):
    def __init__(self):
        self.store = list()

    def add(self, subjects):
        if isinstance(subjects, (list, tuple)):
            self.store.extend(subjects)
        elif isinstance(subjects, str):
            self.store.append(subjects)
        else:
            raise TypeError('only lists, tuples and strings '
                            'of subjects can be added')


class TimeSlots(object):
    """
    Currently only takes # of timeslots until I can figure out a good
    way to standardized time inputs
    """
    def __init__(self, num_slots):
        if isinstance(num_slots, int):
            self.store = num_slots
        else:
            raise TypeError('only accepts number of timeslots as ints')


class Solver(object):
    def __init__(self, teachers, subjects, timeslots):
        if timeslots.store < len(teachers.store):
            raise ValueError('unable to solve for more teachers '
                             'than timeslots')

        self.teachers = teachers.store
        self.subjects = subjects.store
        self.timeslots = timeslots.store
        self.matrix = None
        self.model = None
        self.solver = None
        self.solution = None

    def solve(self):
        self.matrix = Nj.Matrix(len(self.subjects),
                                self.timeslots,
                                len(self.teachers)+1)

        self.model = Nj.Model(
            [Nj.AllDiffExcept0(row) for row in self.matrix.row],
            [Nj.AllDiffExcept0(col) for col in self.matrix.col]
        )

        self.solver = self.model.load('Mistral')
        self.solver.solve()

        self.solution = self.matrix
