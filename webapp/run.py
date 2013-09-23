#!../venv/bin/python

from config import FLASK_PORT_PROD, FLASK_PORT_DEV, PRODUCTION
from controller import app


if __name__ == '__main__':
    if PRODUCTION:
        app.run(debug=False, threaded=True, port=FLASK_PORT_PROD)
    else:
        app.run(debug=True, port=FLASK_PORT_DEV)