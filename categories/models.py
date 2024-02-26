from tea import db
from mongoengine import *
import datetime 

class Category(Document):
    name = StringField(default="")
    status = StringField(default="")
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

class Product(Document):
    name = StringField(required=True)
    category = ReferenceField(Category)
    imgurl=StringField(default="")
    # category =StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)