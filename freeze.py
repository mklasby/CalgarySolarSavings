from flask_frozen import Freezer
from app import *

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()