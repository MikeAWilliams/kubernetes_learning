"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
exaple post
curl --header "Content-Type: application/json" -d '{"delay":4}' http://localhost:36569/stuff
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import pika
import time

logging.basicConfig(level=logging.INFO)


class RabbitWorker:
    def __init__(self):
        self.GetConnection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)

    def GetConnection(self):
        for tryNumber in range(30):
            try:
                logging.info(
                    "Trying to connect to rabbit {}".format(tryNumber))
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='rabbit'))
            except:
                logging.info("caught an exception. waiting one second")
                time.sleep(1)
            else:
                break

    def __del__(self):
        self.connection.close()

    def sendRabbitNewTask(self, delaySeconds):
        message = ' '
        for i in range(delaySeconds):
            message = message + "."
        self.channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        logging.info('Rabbit sent {}\n'.format(message))


globalRabbitWorker = RabbitWorker()


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        bodyRaw = post_data.decode('utf-8')
        logging.info("Body:\n%s\n", bodyRaw)
        bodyDict = json.loads(bodyRaw)
        delay = bodyDict["delay"]
        logging.info("Will post delay:\n%s\n", delay)

        self._set_response()
        self.wfile.write("POST request for {}".format(
            self.path).encode('utf-8'))

        globalRabbitWorker.sendRabbitNewTask(delay)


def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
