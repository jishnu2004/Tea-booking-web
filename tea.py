import json
import sys
import urllib.parse
import os
from flask import Flask, request
from mongoengine import connect
from flask_cors import CORS
tea = Flask(__name__)

CORS(tea)

# db connection
db=connect('tea_db', host='127.0.0.1', port=27017)

from categories import route

# default route
@tea.route("/")
def test():
    return "default"

# @tea.route("/add")
# def add_one():
#     return "success"


if __name__ == "__main__":
   tea.run(host='0.0.0.0', port=5000)