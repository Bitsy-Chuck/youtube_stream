import json
from datetime import datetime

import psycopg2

'''
TODO:
1. Make prepared statements
2. Add log statements
'''


def connect_to_db():
    user = "postgres"
    password = "qwertyui"
    host = "127.0.0.1"
    port = "5432"
    database_name = "fampay"
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database_name,
                                  sslmode='disable')
    cursor = connection.cursor()
    return connection, cursor


def run_evolutions():
    conn, cur = connect_to_db()
    query = "CREATE TABLE if not exists video(" \
            "id bigserial not null, " \
            "title varchar(255) not null, " \
            "description text not null, " \
            "publish_time timestamp not null, " \
            "default_thumbnail_url varchar(255), " \
            "medium_thumbnail_url varchar(255), " \
            "high_thumbnail_url varchar(255), " \
            "constraint pk_video primary key (id)," \
            "constraint uk_title_publish_time unique (title, publish_time)) "
    cur.execute(query)
    conn.commit()


def save_video_info(video_info):
    conn, cur = connect_to_db()
    run_evolutions()
    thumbnails = json.loads(video_info.get('thumbnails'))
    query = "INSERT INTO video(title, description, publish_time, default_thumbnail_url, medium_thumbnail_url, " \
            f"high_thumbnail_url) values('{video_info.get('title')+datetime.today()}', '{video_info.get('desc')}', '{video_info.get('publish_time')}'," \
            f" '{thumbnails.get('default').get('url')}'," \
            f" '{thumbnails.get('medium').get('url')}', '{thumbnails.get('high').get('url')}');"
    print(query)
    cur.execute(query)
    conn.commit()
    print("inserted ", video_info)
