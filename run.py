#!venv/bin/python

from webapp.config import FLASK_PORT_PROD, FLASK_PORT_DEV, PRODUCTION
from webapp import app


if __name__ == '__main__':
    if PRODUCTION:
        app.run(debug=False, threaded=True, port=FLASK_PORT_PROD)
    else:
        app.run(debug=True, port=FLASK_PORT_DEV)