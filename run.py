from cherrypy import wsgiserver
from app import app
import jinja2.ext

if app.debug:
    app.run('0.0.0.0', port=8080, debug=app.debug)
else:
    # from http://flask.pocoo.org/snippets/24/
    d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), d)

    if __name__ == '__main__':
       try:
          server.start()
       except KeyboardInterrupt:
          server.stop()
