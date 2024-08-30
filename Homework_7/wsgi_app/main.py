from wsgi_app.application import Application
from wsgiref.simple_server import make_server


def app(environ, start_response):
    return iter(Application(environ, start_response))

if __name__ == "__main__":
    port = 8000
    server = make_server('0.0.0.0', port, app)
    print(f'Serving on port {port}...')
    server.serve_forever()
