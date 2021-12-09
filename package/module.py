import requests

class Url:
    def __init__(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def open_url(self):
        resp = requests.get(self.url)
        return resp.text
