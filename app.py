from threading import Thread

import psycopg2
from flask import Flask
import fetchVideo as fetchVideo
from apscheduler.schedulers.background import BackgroundScheduler

import consumer

'''
TODO:
1. Create exit handlers
2. 
'''

class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())

scheduler = BackgroundScheduler()
scheduler.start()

# Starts the consumer on a seperate thread bcz channel.start_consuming is a blocking call
thread = Thread(target=consumer.consume)
thread.start()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/fetch/<keyword>')
def fetch(keyword):
    scheduler.add_job(func=fetchVideo.fetch_video, kwargs={"keyword": keyword}, trigger="interval", seconds=10)
    return "done"


if __name__ == '__main__':
    app.run()