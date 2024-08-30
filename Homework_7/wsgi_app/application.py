class Application:

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        path = self.environ.get('PATH_INFO', '/')
        if path == '/':
            return self.handle_root()
        else:
            return self.handle_404()

    @property
    def default_headers(self):
        return [('Content-type', 'text/plain')]

    def handle_root(self):
        body = 'Hello World!'
        status = '200 OK'
        self.start_response(status, self.default_headers)
        yield body.encode()

    def handle_404(self):
        body = '404 Not Found'
        status = '404 Not Found'
        self.start_response(status, self.default_headers)
        yield body.encode()
