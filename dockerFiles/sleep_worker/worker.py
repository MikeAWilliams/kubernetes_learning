#!/usr/bin/env python
import pika
import time
import logging


def callback(ch, method, properties, body):
    logging.info(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    logging.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


class Rabbit_worker:
    def __init__(self):
        self.GetConnection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)

        logging.info(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='task_queue', on_message_callback=callback)
        self.channel.start_consuming()

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


def run():
    worker = Rabbit_worker()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
