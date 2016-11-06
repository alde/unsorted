import logging
from flask import Flask, Response, jsonify, render_template

from . import NAS_UNSORTED
from .files import read_dir, delete_by_hash
from .sorter import sort
from .crossdomain import crossdomain

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/', methods=('GET',))
def index():
    return render_template('index.html')


@app.route('/unsorted', methods=['GET'])
@crossdomain('*')
def unsorted():
    unsorted = read_dir(NAS_UNSORTED)

    return jsonify(unsorted)


@app.route('/delete/<hash>', methods=['DELETE', 'OPTIONS'])
@crossdomain('*')
def delete(hash):
    try:
        delete_by_hash(NAS_UNSORTED, hash)
        return Response('ok', status=200)
    except:
        return Response('Unable to delete', status=500)


@app.route('/sort', methods=['POST'])
@crossdomain('*')
def do_sort():
    try:
        moved = sort(NAS_UNSORTED)
        return jsonify(moved)
    except Exception as e:
        logger.error(e, exc_info=True)
        return Response('Unable to sort', status=500)
