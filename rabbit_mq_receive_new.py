#!/usr/bin/env python
import pika
import sys
from time import sleep

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# channel.exchange_declare(exchange='logs',
#                          exchange_type='fanout')
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

# result = channel.queue_declare(exclusive=True, queue='hello1')

# 生成随机队列名
result = channel.queue_declare(exclusive=True, queue='')
queue_name = result.method.queue
# severities = sys.argv[1:]
# if not severities:
#     print("Usage: %s [info] [warning] [error]" % (sys.argv[0]))
#     sys.exit(1)
# # 只绑定参数中指定的级别的队列
# for severity in severities:
#     channel.queue_bind(exchange='direct_logs',
#                        queue=queue_name,
#                        routing_key=severity)
# channel.queue_bind(exchange='logs',
#                    queue=queue_name)
binding_keys = sys.argv[1:]
if not binding_keys:
    print("Usage: %s [binding_key]" % (sys.argv[0]))
    sys.exit(1)
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body,))


channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)

channel.start_consuming()
