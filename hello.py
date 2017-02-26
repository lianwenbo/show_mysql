import web
from web.ui import app
import sys


web_port = 5000 #web.get_port()
print >>sys.stderr, 'start service at:', web_port
web.run(app, web_port)
