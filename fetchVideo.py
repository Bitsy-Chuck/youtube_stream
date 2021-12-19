import json
import time
from datetime import datetime
from pprint import pprint
import pika
from environs import Env

import googleapiclient.discovery

import Constants
import db
import rmq
from dtos.Thumbnail import Thumbnail
from dtos.VideoInfo import VideoInfo

'''
TODO: 
1. Get latest or after a specific time to avoid duplicates
2. Put variables in .env file 
3. Store scheduler jobs in a job store
4. Encrypt and decrypt API Keys for db storage [FUTURE SCOPE]
'''


def fetch_video(keyword):
    api_service_name = Constants.YOUTUBE_API_SERVICE_NAME
    api_version = Constants.YOUTUBE_API_SERVICE_VERSION
    key = db.fetch_api_key()
    client = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key.api_key)
    request = client.search().list(part="snippet", maxResults=2, type="video", q=keyword)
    resp = request.execute()
    print(f"fetch {keyword} at ", datetime.today())
    # with open("in.txt", 'r') as f:
    #     resp = json.load(f)
    for i in resp.get('items'):
    # for i in resp:
        i = i.get('snippet')
        thumbnail_urls = Thumbnail(i.get("thumbnails").get('default').get('url'),
                                   i.get("thumbnails").get('default').get('url'),
                                   i.get("thumbnails").get('default').get('url'))
        msg = VideoInfo(keyword, i.get('title'), i.get('description'), i.get('publishTime'),
                        thumbnail_urls.toJSON(), key.id)
        rmq.publish_mssg_rmq(msg.toJSON())