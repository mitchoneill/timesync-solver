import unittest
from timesyncsolver.solver import Teachers, Subjects, TimeSlots, Solver


class TestSolver(unittest.TestCase):
    def test_teachers(self):

        teachers = Teachers()
        teachers.add(['Bob', 'Jill', 'Tim', 'Ben'])
        self.assertEqual(len(teachers.store), 4)

        teachers.add('Shane')
        self.assertEqual(len(teachers.store), 5)
        self.assertEqual(teachers.store[4], 'Shane')

        self.assertRaises(TypeError, lambda: teachers.add(1))

    def test_subjects(self):
        subjects = Subjects()
        subjects.add(['Music', 'Art'])
        self.assertEqual(len(subjects.store), 2)

        subjects.add('Sport')
        self.assertEqual(len(subjects.store), 3)
        self.assertEqual(subjects.store[1], 'Art')

        self.assertRaises(TypeError, lambda: subjects.add(1))

    def test_timeslots(self):
        timeslots = TimeSlots(10)
        self.assertEqual(timeslots.store, 10)

        with self.assertRaises(TypeError):
            timeslots = TimeSlots(1.0)

    def test_solver(self):
        teachers = Teachers()
        teachers.add(['Bob', 'Jill', 'Tim', 'Ben'])
        subjects = Subjects()
        subjects.add(['Sport', 'Art'])
        timeslots = TimeSlots(4)

        solver = Solver(teachers,
                        subjects,
                        timeslots)

        solver.solve()

        self.assertEqual(len(solver.solution.row), 2)
        self.assertEqual(len(solver.solution.col), 4)
        self.assertEqual(len(solver.solution.flat), 8)
        self.assertTrue([num in solver.solution.flat for num in
                         range(len(teachers.store)+1)])

        teachers.add('Jeff')
        with self.assertRaises(ValueError):
            solver = Solver(teachers,
                            subjects,
                            timeslots)


if __name__ == '__main__':
    unittest.main()
