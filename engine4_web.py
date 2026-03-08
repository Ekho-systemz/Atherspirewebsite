# Web Server Engine

class WebServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port

    def start(self):
        print(f'Starting server on {self.host}:{self.port}')

    def stop(self):
        print('Stopping server')

    def serve(self, request):
        print(f'Serving request: {request}')

# Example usage:
if __name__ == '__main__':
    server = WebServer()
    server.start()
    server.serve('GET /')
    server.stop()