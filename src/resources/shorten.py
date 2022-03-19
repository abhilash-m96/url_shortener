from flask import request
from flask_restful import Resource
from models.url_shortener_model import URLShortenerMapping
import hashlib
import validators


class Shorten(Resource):
    def __init__(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        payload = request.get_json()
        input_url = payload.get("url")

        valid_url = validators.url(input_url)
        if not valid_url:
            return {
                "response": False,
                "message": f"Input URL: '{input_url}' is not valid URL",
            }

        short_id = self.generate_short_id(input_url)
        shortened_url = request.root_url + short_id

        # Storing the url_shortener mapping to the db
        try:
            url_shortener_mapping = URLShortenerMapping(
                input_url=input_url, id=short_id
            )
            url_shortener_mapping.save()
            return {
                "response": True,
                "input_url": input_url,
                "shortened_url": shortened_url,
            }
        except Exception as e:
            print("Failed to insert to DB")
            print(str(e))

        return ({"response": False, "message": "Failed to shorten the URL"},)

    @staticmethod
    def generate_short_id(input_url: str, num_of_chars: int = 6):
        md5sum_hash = hashlib.md5(input_url.encode("utf-8")).hexdigest()
        shortened_code = md5sum_hash[:6]
        return shortened_code
