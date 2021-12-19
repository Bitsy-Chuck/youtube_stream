import json

import pika

import Constants
import db
import rmq
import sys
import threading

'''
TODO:
1. Add message retry
'''
_conn,_channel = None, None
def get_rmq_conn_consumer():
    global _conn, _channel
    _conn = pika.BlockingConnection(pika.ConnectionParameters(host=Constants.RMQ_HOST))
    _channel = _conn.channel()
    _channel.queue_declare(queue=Constants.QUEUE_NAME, durable=True)

def init_rmq_conn_consumer():
    if _conn is None or _channel is None or _channel.is_closed:
        get_rmq_conn_consumer()
    return _conn, _channel

def consume():
    init_rmq_conn_consumer()
    _channel.basic_consume(queue=Constants.QUEUE_NAME, on_message_callback=process, auto_ack=True)
    try:
        _channel.start_consuming()
    except Exception as e:
        print(sys.exc_info()[2])
        print("failed to consume: ", e)
    threading.currentThread()
    print("done")


def process(ch, method, properties, message):
    print("Got the message", message)
    video_info = json.loads(message)
    db.save_video_info(video_info)
