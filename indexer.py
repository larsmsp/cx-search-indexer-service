# coding=utf-8
import logging

from flask import Flask, request
from google.appengine.api import search

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)


@app.route('/put', methods=['POST'])
def index():
    data = request.get_json()
    documents = [search.Document(doc_id=d['id'], fields=[
        search.TextField(name='title', value=d['title']),
        search.TextField(name='contents', value=d['contents']),
        search.TextField(name='url', value=d['url'])
    ]) for d in data]
    index = search.Index('computas-docs')
    results = index.put(documents)
    document_ids = [d.id for d in results]
    return "Added documents: {0}".format(', '.join(document_ids))
