from cherrypy import wsgiserver
from app import create_app
import jinja2.ext

if __name__ == '__main__':
    app = create_app('config.BaseConfiguration')
    if app.debug:
        app.run('0.0.0.0', port=8080, debug=app.debug)
    else:
        # from http://flask.pocoo.org/snippets/24/
        d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
        server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), d)

        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()
