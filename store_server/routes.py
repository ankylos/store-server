from flask import Blueprint, request
import pymongo

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    return 'OK', 200

@main.route('/webhook', methods=['POST'])
def receive_webhook():
    key = request.GET.get('key', '')

    if not key:
        return 'Invalid Request', 403

    if key != 'ef47e2f3d598da95dd183c059a0baedf':
        return 'Invalid Credentials', 403

    return 'OK', 200

