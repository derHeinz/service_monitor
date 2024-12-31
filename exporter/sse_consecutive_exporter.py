from queue import Queue
import json
import os
import logging
import time

from flask.wrappers import Response
from flask.json import jsonify

from flask import Flask, make_response, send_from_directory, request
from werkzeug.serving import make_server
from threading import Thread

logger = logging.getLogger(__file__)


class _WebServer(Thread):

    def __init__(self):
        """Create a new instance of the flask app"""
        super(_WebServer, self).__init__()

        self.messages = Queue()
        self.service_callback = None

        self.app = Flask(__name__)
        self.app.config['port'] = 5678
        self.app.config['app_name'] = "Server Sent Events Exporter"
        self.app.app_context().push()

        self._server = make_server(host='0.0.0.0', port=self.app.config['port'], app=self.app, threaded=True)
        print("Starting %s on port %d" % (self.app.config['app_name'], self.app.config['port']))

        # register some endpoints
        self.app.add_url_rule(rule="/", view_func=self.index, methods=['GET'])
        self.app.add_url_rule(rule="/files/<path:path>", view_func=self.files, methods=['GET'])
        self.app.add_url_rule(rule="/stream", view_func=self.stream)
        self.app.add_url_rule(rule="/request_update", view_func=self.request_update, methods=['POST'])

        # register default error handler
        self.app.register_error_handler(code_or_exception=404, f=self.not_found)

    def send_message(self, data):
        self.messages.put(data)

    def _get_message(self):
        return self.messages.get()

    def get_message(self):
        '''this could be any function that blocks until data is ready'''
        time.sleep(1.0)
        s = time.ctime(time.time())
        return s

    def run(self):
        self._server.serve_forever()

    def not_found(self, error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    def index(self):
        """Serve the main index page"""
        return send_from_directory('sse_consecutive_exporter', 'metro-sse-index.html')

    def files(self, path):
        """Serve files from the static directory"""
        return send_from_directory(os.path.join('sse_consecutive_exporter', 'files'), path)

    def stream(self):
        logger.info("attached a listener to receive SSEs.")

        def eventStream():
            while True:
                # wait for source data to be available, then push it
                yield 'data: {}\n\n'.format(self._get_message())
        resp = Response(eventStream(), headers={}, mimetype="text/event-stream")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    def request_update(self):
        requested_service_name = request.data.decode('utf-8')
        logger.info("received request to update: " + requested_service_name)
        self.service_callback(requested_service_name)
        return 'Success'


class SSEConsecutiveExporter(object):

    def __init__(self, **kwargs):
        self.server = _WebServer()
        self.server.setDaemon(True)
        self.server.start()

    def export(self, service):
        keys_to_export = ['service_name', 'service_config', 'service_state', 'service_info', 'service_time']
        exportable = {key: service[key] for key in keys_to_export}

        json_string = json.dumps(exportable)
        self.server.send_message(json_string)

    def set_worker_callback(self, service_worker_callback):
        self.server.service_callback = service_worker_callback
