import os
import imp
import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

def load_plugins(folder):
	plugins = []
	for p in sorted(os.listdir(folder)):
		if p.endswith('.py'):
			m = p[:-3]
			info = imp.find_module(m, [folder])
			plugins.append(imp.load_module(m, *info))
	return plugins

class AlfredWs(WebSocket):
	def received_message(self, message):
		if message.is_binary:
			return #just ignore it
		m = message.data.decode("utf-8")
		f = m.split(" ")[0]
		handled = False
		for p in plugins:
			if hasattr(p, f):
				r = getattr(p, f)(self) #FIXME
				if r:
					handled = True
					self.send("done")
					break
		if not handled:
			self.send("unknown")

class Root(object):
	def __init__(self):
		with open("index.html", "r") as f:
			self.static_content = f.read()
	@cherrypy.expose
	def index(self):
		return self.static_content
	@cherrypy.expose
	def ws(self):
		handler = cherrypy.request.ws_handler

plugins = load_plugins('plugins') #FIXME
cherrypy.config.update({'server.socket_port': 8080})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

c = {'/ws': {'tools.websocket.on': True, 'tools.websocket.handler_cls': AlfredWs}}
cherrypy.quickstart(Root(), '/', config=c)
