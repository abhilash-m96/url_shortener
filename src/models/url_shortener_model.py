import mongoengine as me
import datetime


class URLShortenerMapping(me.Document):
    meta = {"collection": "url_shortener_mappings"}
    id = me.StringField(primary_key=True)
    input_url = me.URLField(required=True)
    created_at = me.DateTimeField(default=datetime.datetime.utcnow)
