from flask import Blueprint, request
import pymongo

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    return 'OK', 200

@main.route('/message')
def receive_message():
    return 'OK', 200

