import threading
import socket
from gevent.pywsgi import WSGIServer

_apps = {}


def run(app, port):
    #server = WSGIServer(('101.37.30.109', port), app)
    server = WSGIServer(('', port), app)
    if port not in _apps:
        _apps[port] = server
    server.serve_forever()


def start(app, port=0):
    if port == 0:
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
    if port in _apps:
        return
    t = threading.Thread(target=run, args=(app, port))
    t.daemon = True
    t.start()
    return port


def get_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def stop(port):
    server = _apps.get(port, None)
    if server is not None:
        server.stop()
