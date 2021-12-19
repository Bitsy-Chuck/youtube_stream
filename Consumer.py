import json
import Constants
import db
import rmq

'''
TODO:
1. Add message retry
'''
def consume():
    channel, _conn = rmq.get_rmq_conn()
    channel.basic_consume(queue=Constants.QUEUE_NAME, on_message_callback=process, auto_ack=True)
    channel.start_consuming()
    print("done")


def process(ch, method, properties, message):
    print("Got the message", message)
    video_info = json.loads(message)
    db.save_video_info(video_info)
