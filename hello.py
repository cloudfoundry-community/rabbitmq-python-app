#!/usr/bin/env python
from flask import Flask
import json
import os
import pika
import logging
import sys

#For Logging
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)
#ch = logging.StreamHandler(sys.stderr)
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#log.addHandler(ch)

app = Flask(__name__)

port = int(os.getenv("PORT", 9099))

@app.route('/')
def hello_world():
    #Getting Service Info
    env_vars = os.getenv('VCAP_SERVICES')
    rmq_service = str(os.getenv('RMQ_SERVICE', 'p-rabbitmq-36'))
    service = json.loads(env_vars)['rabbitmq-36'][0]
    amqp_url = service['credentials']['protocols']['amqp']['uri']

    #For Sending
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='OK')
    connection.close()

    #For Receiving
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    method_frame, header_frame, body = channel.basic_get(queue = 'hello')
    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        return body

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
