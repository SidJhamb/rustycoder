import celery
from celery import Celery
import os


# Create the app and set the broker location (RabbitMQ)
app = Celery('Worker',
             backend='pyamqp://guest@localhost//',
             broker='pyamqp://guest@localhost//')

@app.task
def long_task(url):
    print url

