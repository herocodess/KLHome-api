import pymongo
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import datetime
import json
import itertools
from pymongo import MongoClient
from bson import ObjectId, json_util


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

# client = MongoClient('192.168.137.52:27017')
# db = client.appliances

# app.config['MONGO_URI'] = "mongodb://192.168.137.52:27017/appliances"
myClient = pymongo.MongoClient("mongodb://172.16.11.162:27017/")
myDb = myClient["appliances"]/
myCol = myDb["toggle"]
# mongo = PyMongo(app)
# app.json_encoder = JSONEncoder

GPIO.setmode(GPIO.BCM)
# create a dictionary called pins to store the pin number , name and pin state
pins = {
    23 : {
        'pin_no' : 23,
        'name':'GPIO 23',
        'state': GPIO.HIGH
    }
}

# set each pin as an output and make it low
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def main():
    # for each pin, read the pin state and store it in the pins dictionary
    for p in pins:
        pins[p]['state'] = GPIO.input(p)
    # put tje pin dictionary into the template data dictionary
    templateData = {
        'pins':pins
    }
    #return template data as JSON
    return jsonify({'message': templateData})

    #the function below is executed when someone requests a URL with the pin number and action in it

@app.route('/togglelight', methods=['POST'])
def action():
    request_data = request.get_json()
    #convert the pin from the URL into an integer
    print(type(request_data))
    #changePin = (d['changePin'])
    #print(type(request_data))
    for i in request_data:
        changePin = i['changePin']
        action = i['action']

    #get the device name from the pin being changed
    deviceName = pins[changePin]['name']

    #action = request_data['action']
    #if the action part of the URL is "on", execute the code below
    if action == "off":
        #set the pin high
        GPIO.output(changePin, GPIO.HIGH)
        #save the status message to be passed into the template
        message = "Turned " + deviceName + " off."
    if action == "on":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " on."
    #for each pin, read the pin state and store it into a dictionary
    pins[23]['state'] = GPIO.input(23)

    #along with the pin dictionary, put the message into the template data dictionary
    nTemplateData = pins[23]    
    #mongo.db.toggle.insert_one(nTemplateData)
    #myCol.insert_one(nTemplateData)

    data = json.dumps(nTemplateData, default=json_util.default)
    d = json.loads(data)
    myCol.insert(d)
    # mongo.db.toggle.insert_one(d)
    return jsonify({'data': data, 'message': message}), 201

if __name__ == '__main__':
    app.run(host='172.16.11.161', port=5000, debug=True)    