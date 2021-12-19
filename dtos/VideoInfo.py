import json


class VideoInfo:
    def __init__(self, video_title, desc, publish_time, thumbnails):
        self.title = video_title
        self.desc = desc
        self.publish_time = publish_time
        self.thumbnails = thumbnails

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
