import json
import pika
import db


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='queue_name', on_message_callback=process, auto_ack=True)
    channel.start_consuming()
    print("done")


def process(ch, method, properties, message):
    print("Got the message", message)
    video_info = json.loads(message)
    db.save_video_info(video_info)
