import json
from datetime import datetime
from environs import Env
import environs
import psycopg2

from dtos.ApiKeyResponse import ApiKeyResponse

'''
TODO:
1. Make prepared statements
2. Add log statements
'''

_conn, _cur = None, None
env = Env()
env.read_env()


def init_conn_db():
    global _conn, _cur
    user = env.str('DB_USER_NAME')
    password = env.str("DB_PASSWORD")
    host = env.str("DB_HOST")
    port = env.str("DB_PORT")
    database_name = env.str("DB_NAME")
    _conn = psycopg2.connect(user=user,
                             password=password,
                             host=host,
                             port=port,
                             database=database_name,
                             sslmode='disable')
    _cur = _conn.cursor()
    return _conn, _cur


def get_db_conn():
    return _conn, _cur


def run_evolutions():
    query = """
        CREATE TABLE IF NOT EXISTS key_metadata(
        id bigserial not null,
        api_key varchar(255) not null,
        max_quota int not null, 
        consumed_quota int not null, 
        created_at timestamp DEFAULT CURRENT_TIMESTAMP::TIMESTAMP(0) NOT NULL, 
        last_fetch timestamp,
        config json,
        constraint pk_metadata primary key (id),
        constraint uk_metadata_api_key unique (api_key));
        """
    query += "CREATE TABLE if not exists video(" \
             "id bigserial not null, " \
             "keyword varchar(255) not null," \
             "title varchar(255) not null, " \
             "description text not null, " \
             "publish_time timestamp not null, " \
             "default_thumbnail_url varchar(255), " \
             "medium_thumbnail_url varchar(255), " \
             "high_thumbnail_url varchar(255), " \
             "fetched_from_key int not null," \
             "constraint pk_video primary key (id)," \
             "constraint uk_video_title_publish_time unique (title, publish_time)," \
             "constraint fk_video_metadata foreign key (fetched_from_key) references key_metadata(id) on delete " \
             "cascade ); "

    try:
        commit_to_db(query)
    except Exception as e:
        print("Unable to apply evolutions")
        raise IOError("Failed to apply evolutions", e)


def save_video_info(video_info):
    thumbnails = json.loads(video_info.get('thumbnails'))
    query = f"""
    INSERT INTO video(keyword, title, description, publish_time, default_thumbnail_url, medium_thumbnail_url,
    high_thumbnail_url, fetched_from_key) 
    values('{video_info.get('keyword')}',
     '{video_info.get('title') + str(datetime.today())}',
     '{video_info.get('desc')}', 
     '{video_info.get('publish_time')}',
     '{thumbnails.get('default')}',
     '{thumbnails.get('medium')}',
     '{thumbnails.get('high')}',
     '{video_info.get("fetched_from_key")}'
     );
    """
    print(query)
    commit_to_db(query)
    print("inserted ", video_info)


def commit_to_db(query):
    try:
        _cur.execute(query)
        _conn.commit()
    except Exception as e:
        print("Failed to execute query", e)


# TODO: Implement redis cache to prevent DB call every 10 sec
def fetch_api_key():
    query = """
    select id, api_key, consumed_quota, max_quota from key_metadata where consumed_quota < max_quota order by last_fetch limit 1;
    """

    _cur.execute(query)
    res = _cur.fetchone()
    if res is None:
        raise IOError("No Key found")
    fetch_time = str(datetime.today())
    query = f"""
    update key_metadata set last_fetch='{fetch_time}', consumed_quota={res[2]+1} where api_key = '{res[1]}';
    """
    print(query)
    try:
        commit_to_db(query)
    except Exception as e:
        raise IOError("Failed to fetch API keys")
    return ApiKeyResponse(id=res[0], api_key=res[1], consumed_quota=res[2], max_quota=res[3])


def get_latest_videos(keyword):
    # TODO: Get paginated response
    query = f"""
    select * from video where keyword = {keyword} order by publish_time desc;
    """
    _cur.execute(query)
    res = _cur.fetchall()
    return json.dump(res)


def close_connection():
    _conn.close()
