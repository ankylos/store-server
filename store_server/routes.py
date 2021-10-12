import os

from flask import Blueprint, request
import pymongo

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    return 'OK', 200

@main.route('/webhook', methods=['POST'])
def receive_webhook():
    webhook_key = os.getenv('key', '')

    key = request.args.get('key', '')

    if not key:
        return 'Invalid Request', 403

    if key != webhook_key:
        return 'Invalid Credentials', 403

    return 'OK', 200

