from flask_restful import Resource
from flask import redirect
from models.url_shortener_model import URLShortenerMapping


class URLRedirector(Resource):
    def get(self, *args, **kwargs):
        short_id = kwargs.get("shortened_id")
        url_mapping = URLShortenerMapping.objects(id=short_id).first()
        if not url_mapping:
            return {"response": False, "message": "Invalid URL"}, 400

        actual_url = url_mapping.input_url
        return redirect(actual_url)
