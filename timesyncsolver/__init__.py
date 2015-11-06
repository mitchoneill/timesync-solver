from flask import Flask
import logging

log = logging.getLogger(__name__)
app = Flask(__name__)

from timesyncsolver.receiver import solver

if __name__ == '__main__':
    app.run()
