import inspect
import os
import time
import eventlet
import socket
import socketio
import webbrowser
import json


__version__ = "0.1.0"


class WebConsole:
	def __init__(self, host="127.0.0.1", port=8080, show_url=True, debug=False):
		self.host = host
		self.port = port
		self.debug = debug
		self.history = []
		self.clients = []
		cur_path = os.path.dirname(os.path.realpath(__file__))
		self.sio = socketio.Server()
		self.app = socketio.WSGIApp(self.sio, static_files={
			'/': {'content_type':'text/html','filename': os.path.join(cur_path,'web','index.html')},
			'/static': os.path.join(cur_path,'web')
		}, socketio_path='/socket.io')

		self.sio.on('connect', self.on_connect)
		self.sio.on('disconnect', self.on_disconnect)
		self.sio.on('get_history', self.on_get_history)

		self.sio.start_background_task(target=self.start)
		if show_url: print(f"Web Console: {self.url}")

	def start(self):
		eventlet.wsgi.server(eventlet.listen((self.host, self.port)), self.app, log_output=self.debug)

	@property
	def url(self):
		ip_address = socket.gethostbyname(socket.gethostname()) if self.host == "0.0.0.0" else self.host
		return f"http://{ip_address}:{self.port}/"

	def open(self): webbrowser.open(self.url)
	def sleep(self, s): self.sio.sleep(s)
	def loop(self):
		try:
			while True:
				self.sleep(1)
		except KeyboardInterrupt: None

	def on_connect(self, sid, environ):
		self.clients.append(sid)

	def on_disconnect(self, sid):
		self.clients.remove(sid)

	def on_get_history(self, sid):
		return self.history

	def emit(self, event, data, client=None):
		eventlet.spawn(self.sio.emit, event, data, to=client)

	def jsonable(self, x):
		try:
			json.dumps(x)
			return True
		except:
			return False

	def log(self, message, log_level="info"):
		def get_frame():
			current_file = os.path.realpath(__file__)
			stack = inspect.stack()
			for frame in stack:
				if frame.filename != current_file:
					return frame

		frame = get_frame()
		line_number = frame.lineno
		full_path = frame.filename
		file_with_ext = os.path.basename(full_path)
		file_name = os.path.splitext(file_with_ext)[0]

		data = {
			"level": log_level,
			"time": int(time.time()),
			"message": message if self.jsonable(message) else str(message),
			"filename": file_name,
			"file_path": full_path,
			"line": line_number
		}
		self.history.append(data)
		self.emit('new_log', data)

	def warn(self, message): self.log(message, "warn")
	def error(self, message): self.log(message, "error")
