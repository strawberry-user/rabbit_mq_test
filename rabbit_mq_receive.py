#!/usr/bin/env python
import pika
from time import sleep

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

# 队列声明为持久化
channel.queue_declare(queue='durable_hello', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    sleep(str(body).count('.'))
    print(" [x] Done")
    # 确认，如果忘记的话，没响应的消息就一直不能释放
    channel.basic_ack(delivery_tag=method.delivery_tag)


# 在同一时刻，不要发送超过1条消息给一个工作者（worker），直到它已经处理了上一条消息并且作出了响应
channel.basic_qos(prefetch_count=1)

# 需要确认，可以防止消费者挂掉后其正在处理的消息丢失的情况
channel.basic_consume(on_message_callback=callback, queue='hello')

# 不需要确认
# channel.basic_consume(on_message_callback=callback, queue='hello', auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
