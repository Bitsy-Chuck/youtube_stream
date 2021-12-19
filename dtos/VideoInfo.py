import json


class VideoInfo:
    def __init__(self, keyword, video_title, desc, publish_time, thumbnails, fetched_from_key):
        self.keyword = keyword
        self.title = video_title
        self.desc = desc
        self.publish_time = publish_time
        self.thumbnails = thumbnails
        self.fetched_from_key = fetched_from_key

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
