import os
from flask import Flask, request
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = os.getenv('RABBITMQ_CONNECTION')
    app.config['CELERY_RESULT_BACKEND'] = os.getenv('RABBITMQ_CONNECTION')

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    @app.route('/')
    def index():
        return 'OK', 200

    @app.route('/webhook', methods=['POST'])
    def receive_webhook():
        webhook_key = os.getenv('key', '')

        key = request.args.get('key', '')

        if not key:
            return 'Invalid Request', 403

        if key != webhook_key:
            return 'Invalid Credentials', 403

        task = process_message.AsyncResult(key)

        return 'OK', 200

    @app.route('/process', methods=['POST'])
    def process_message():
        task = process_html.apply_async()
        return url_for('receive_webhook', task_id=task.id)

    @celery.task
    def process_html(key):
        from pymongo import MongoClient

        MONGODB_CONNECTION = os.getenv('MONGODB_CONNECTION', '')

        client = MongoClient(MONGODB_CONNECTION)
        database = client['ankylos-crawl-db']
        src_collection = database['temp-crawl-results']

        item = collection.find_one({'key':key})

        if not item:
            return f"No doc found for {key}"

        dest_collection = database['store-repository']
        dest_collection.create_index('key', unique=True)

        dest_collection.insert_one(item)

        return {'status':'Task Completed', 'is_completed':True}

    return app
