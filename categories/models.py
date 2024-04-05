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


# New model for different project

class Organizations(Document):
    org_id = StringField(default="")
    org_name = StringField(default="")
    description = StringField(default="")
    created_person = StringField(default="")
    status = StringField(default="active")
    source = StringField(default="")
    type = StringField(default="")
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    updated_date = DateTimeField(default=datetime.datetime.utcnow)

class Location(Document):
    org=ReferenceField(Organizations)
    locationName=StringField(default="")
    country=StringField(default="")
    state=StringField(default="")
    city=StringField(default="")
    zipCode=StringField(default="")
    latitude=IntField()
    longitude=IntField()

class CustomerGroup(Document):
    location=ReferenceField(Location)
    customer_group_name=StringField(default="")

class Customers(Document):
    customer_group=ReferenceField(CustomerGroup)
    customer_name=StringField(default="")
    customer_email=StringField(default="")
    customer_phone=StringField(default="")

# latest models
    
class Categories(Document): 
    category_id=StringField(default="")
    org_id = ReferenceField(Organizations)
    str_org_id = StringField(default="")
    parent_id= StringField(default="")
    name = StringField(default="")
    description = StringField(default="")
    status = StringField(default="active")
    CreatedTimestamp = DateTimeField(default=datetime.datetime.utcnow)
    
class Products(Document): 
    product_id=StringField(default="")
    org_id = ReferenceField(Organizations)
    product_name = StringField(default="")
    product_description = StringField(default="")
    status = StringField(default="active")
    CreatedTimestamp = DateTimeField(default=datetime.datetime.utcnow)    
    
class PrizeList(Document): 
    prizelist_id=StringField(default="")
    org_id = ReferenceField(Organizations)
    product_id = ReferenceField(Products)
    str_product_id = StringField(default="")
    product_name = StringField(default="")
    prize= StringField(default="")
    tax= StringField(default="")
    status = StringField(default="active")
    CreatedTimestamp = DateTimeField(default=datetime.datetime.utcnow)   

class Tax(Document): 
    tax_id=StringField(default="")
    org_id = ReferenceField(Organizations)
    tax_amount=StringField(default="")
    prizelist_id = ReferenceField(PrizeList)
    status = StringField(default="active")
    CreatedTimestamp = DateTimeField(default=datetime.datetime.utcnow) 
