from threading import Thread

from environs import Env
from flask import Flask

import db
import fetchVideo as fetchVideo
from apscheduler.schedulers.background import BackgroundScheduler

import Consumer
import rmq

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
thread = None

def start_consumer():
    global thread
    # Starts the consumer on a separate thread bcz channel.start_consuming is a blocking call
    thread = Thread(target=Consumer.consume)
    thread.start()
@app.before_first_request
def init():
    db.init_conn_db()
    db.run_evolutions()
    rmq.init_rmq_conn()
    start_consumer()
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/fetch/<keyword>')
def fetch(keyword):
    scheduler.add_job(func=fetchVideo.fetch_video, kwargs={"keyword": keyword}, trigger="interval", seconds=10)
    return "done"

@app.route('/video/info')
def get_videos():
    res = db.get_latest_videos()
    return res

def clean_up():
    thread.join()
    scheduler.shutdown()
    db.close_connection()
    rmq.close_rmq_conn()


if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        clean_up()
        print("Exiting")