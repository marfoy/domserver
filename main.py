import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

class AlfredWs(WebSocket):
	def received_message(self, message):
		if message.is_binary:
			return #just ignore it
		m = message.data.decode("utf-8")
		print m
		#self.send("err wut?")

cherrypy.config.update({'server.socket_port': 8080})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

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

c = {'/ws': {'tools.websocket.on': True, 'tools.websocket.handler_cls': AlfredWs}}
cherrypy.quickstart(Root(), '/', config=c)
