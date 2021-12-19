import pika

import Constants

_channel = None
_conn = None
def init_rmq_conn():
    global _channel, _conn
    _conn = pika.BlockingConnection(pika.ConnectionParameters(host=Constants.RMQ_HOST))
    _channel = _conn.channel()
    _channel.queue_declare(queue=Constants.QUEUE_NAME, durable=True)

def get_rmq_conn():
    return _channel, _conn


def publish_mssg_rmq(mssg):
    _channel.basic_publish(exchange=Constants.EXCHANGE_NAME, routing_key=Constants.QUEUE_NAME, body=mssg)
    print("published ", mssg)


def close_rmq_conn():
    global _channel, _conn
    _channel.stop_consuming()
    _conn.close()
