from timesyncsolver import app
import Numberjack as Nj
from flask import request, jsonify
from timesyncsolver.solver import Teachers, Subjects, TimeSlots, Solver
import logging

log = logging.getLogger(__name__)


@app.route('/', methods=['POST'])
def solver():
    req_json = request.json

    teachers = Teachers()
    teachers.add(req_json['teachers'])
    subjects = Subjects()
    subjects.add(req_json['subjects'])
    timeslots = TimeSlots(req_json['timeslots'])

    solver = Solver(teachers, subjects, timeslots)
    solver.solve()

    result = solver.solution
    result = [[int(str(e)) for e in row] for row in result.row]

    return jsonify(data=result)
