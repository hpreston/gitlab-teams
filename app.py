#! /usr/bin/env python

import os
from flask import Flask, request
from flask_restful import Resource, Api
from ciscosparkapi import CiscoSparkAPI
from events import event_handler
app = Flask(__name__)
api = Api(app)
spark = CiscoSparkAPI()
room_id = os.getenv("SPARK_ROOM")

class Notify(Resource):
    def get(self):
        return "hello"

    def post(self):
        msg = event_handler(request.json)
        print ("sending {}".format(msg))
        message = spark.messages.create(room_id, markdown=msg)

        return {'hello': 'world'}

api.add_resource(Notify, '/notify')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
