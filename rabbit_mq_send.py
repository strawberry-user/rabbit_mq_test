#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.queue_declare(queue='durable_hello', durable=True)

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=bytes(message, encoding='utf8'),
                      properties=pika.BasicProperties(
                          delivery_mode=2  # make message persistent
                      ))
connection.close()
