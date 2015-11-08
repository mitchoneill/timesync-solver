from flask import request, jsonify, abort, Flask
from timesyncsolver.solver import Teachers, Subjects, TimeSlots, Solver

app = Flask(__name__)


@app.before_first_request
def setup_logging():
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        try:
            file_handler = RotatingFileHandler('logs/solver.log', 'a', 1 * 1024 * 1024, 10)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('solver startup')
        except Exception as e:
            print e


@app.route('/', methods=['POST'])
def solver():
    req_json = request.json

    teachers = Teachers()
    teachers.add(req_json['teachers'])
    subjects = Subjects()
    subjects.add(req_json['subjects'])
    timeslots = TimeSlots(len(req_json['teachers']))

    solver = Solver(teachers, subjects, timeslots)
    solver.solve()

    result = solver.solution

    try:
        data = dict(zip(req_json['subjects'], [map((lambda element: req_json['teachers'][element]), subject) for subject in [[int(str(e)) for e in row] for row in result.row]]))
    except Exception as e:
        app.logger.error("Couldn't solve model. Error: {0}".format(e))
        abort(500)
    else:
        app.logger.info("Solved model with {0} teachers and {1} subjects"
                        .format(len(req_json['teachers']), len(req_json['subjects'])))
        return jsonify(data=data)

if __name__ == '__main__':
    app.run()
