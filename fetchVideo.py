import json
import time
from datetime import datetime
from pprint import pprint
import pika

import googleapiclient.discovery

from dtos.VideoInfo import VideoInfo

'''
TODO: 
1. Get latest or after a specific time to avoid duplicates
2. Put variables in .env file 
3. Store scheduler jobs in a job store
'''

def fetch_video(keyword):
    api_service_name = 'youtube'
    api_version = 'v3'
    API_KEY = 'AIzaSyA8X2GRCuphXvyDp5j_Uep4Abv9cNQz0PM'
    # client = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY)
    # request = client.search().list(part="snippet", maxResults=2, type="video", q=keyword)
    # resp = request.execute()
    print(f"fetch {keyword} at ", datetime.today())
    with open("in.txt", 'r') as f:
        resp = json.load(f)
    # for i in resp.get('items'):
    for i in resp:
        i = i.get('snippet')
        thumbnail_urls = {"default": i.get("thumbnails").get('default'), "medium": i.get("thumbnails").get('medium'),
                          "high": i.get("thumbnails").get('high')}
        mssg = VideoInfo(i.get('title'), i.get('description'), i.get('publishTime'), json.dumps(thumbnail_urls))
        publish_mssg_rmq(mssg.toJSON())


def get_rmq_conn():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='queue_name', durable=True)
    return channel, connection


def publish_mssg_rmq(mssg):
    channel, conn = get_rmq_conn()
    channel.basic_publish(exchange="", routing_key='queue_name', body=mssg)
    print("published ", mssg)
    conn.close()