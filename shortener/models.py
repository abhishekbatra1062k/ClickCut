from django.conf import settings

class URLMapping:
    collection = settings.MONGO_DB["urls"]

    @staticmethod
    def save_url_mapping(short_url, long_url):
        URLMapping.collection.insert_one({"short_url": short_url, "long_url": long_url})

    @staticmethod
    def get_long_url(short_url):
        result = URLMapping.collection.find_one({"short_url": short_url})
        return result["long_url"] if result else None
