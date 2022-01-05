#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or "Hello World!"
channel = connection.channel()

# severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
# 扇形交换机
# channel.exchange_declare(exchange='logs',
#                          exchange_type='fanout')

# 直连交换机
# channel.exchange_declare(exchange='direct_logs',
#                          exchange_type='direct')

# 主题交换机
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

# result = channel.queue_declare(exclusive=True)
# channel.queue_bind(exchange='logs',
#                    queue=result.method.queue)
channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=bytes(message, encoding='utf8'))
connection.close()
