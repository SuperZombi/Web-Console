import inspect
import os
import time
import eventlet
import socket
import socketio


def log_message(message):
	frame = inspect.currentframe()
	caller_frame = frame.f_back
	line_number = caller_frame.f_lineno
	file_path = caller_frame.f_code.co_filename
	file_full_name = os.path.basename(file_path)
	file_name = os.path.splitext(file_full_name)[0]
	
	print(f"{message} ({file_name}:{line_number})")


class WebConsole:
	def __init__(self, host="127.0.0.1", port=8080):
		self.host = host
		self.port = port
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
		print(f"Running on {self.url}")

	def start(self):
		eventlet.wsgi.server(eventlet.listen((self.host, self.port)), self.app, log_output=False)

	@property
	def url(self):
		ip_address = socket.gethostbyname(socket.gethostname()) if self.host == "0.0.0.0" else self.host
		return f"http://{ip_address}:{self.port}/"

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

	def log(self, message):
		frame = inspect.currentframe()
		caller_frame = frame.f_back
		line_number = caller_frame.f_lineno
		file_path = caller_frame.f_code.co_filename
		file_full_name = os.path.basename(file_path)
		file_name = os.path.splitext(file_full_name)[0]

		data = {
			"type": "log",
			"time": int(time.time()),
			"message": message,
			"filename": file_name,
			"line": line_number
		}
		self.history.append(data)
		self.emit('new_log', data)
		print(f"{message} ({file_name}:{line_number})")
