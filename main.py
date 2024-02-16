from pymongo import MongoClient
import pprint


# Connecting to mongodb compass
connection_string="mongodb://localhost:27017"
client=MongoClient(connection_string)

dbs=client.list_database_names()
print(dbs) #listing all database

test_db=client.mydb
collections=test_db.list_collection_names()
print(collections)



# Inserting one document to collection/table in mongodb
def insert_test_doc():
    collection=test_db.test
    test_document={
        "name":"jishnu",
        "type":"myname"
    }
    inserted_id=collection.insert_one(test_document).inserted_id  # every document has unique id
    print(inserted_id)

insert_test_doc()


# Inserting many documents together
collection=test_db.test
def creat_document():
    first_name=["jishnu","vishnu","ganga","thushara"]
    last_name=["prakash","prakash","s","m g"]
    age=[21,25,18,34]

    docs=[]

    for first_name,last_name,age in zip(first_name,last_name,age):
        doc={"first_name":first_name,"last_name":last_name,"Age":age}
        docs.append(doc)

    collection.insert_many(docs)

creat_document()



# For better format printing
printer=pprint.PrettyPrinter() 

#  Reading documents
def reading_collection():
    x=collection.find()
    for i in x:
        printer.pprint(i)

reading_collection()


# finding specific document
def find_element():
    x=collection.find_one({"first_name":"thushara","last_name":"m g"})
    # finding based on first and last name
    printer.pprint(x);

find_element()


# Counting number of document with /without condition'

def total_count():
    tc=collection.count_documents(filter={})
    # c=collection.find().count()
    print("Number of document in test collection is: ",tc)
    # print(c)

total_count()

# Getting document using ID

def get_element_by_id(person_id):
    from bson.objectid import ObjectId
    _id=ObjectId(person_id)
    # above step convert some string to proper id format
    x=collection.find_one({"_id":_id})
    printer.pprint(x)

get_element_by_id("65cf386a5d6f2d5e70d6e5a9")



# getting people with in some age range

def get_age_range(min_age,max_age):
    query={"$and":[
            {"Age":{"$gte":min_age}}, #gte=>greater than equal to ,lte=>less than equal to
            {"Age":{"$lte":max_age}}
        ]
    }
    people=collection.find(query).sort("Age")
    for i in people:
        printer.pprint(i)


get_age_range(18,25)


# UPDATING one document using id 
from bson.objectid import ObjectId
def update_person_by_id(person_id):
    _id=ObjectId(person_id)
    updates={
        "$set":{"new_field":True},
        "$inc":{"Age":1},
        "$rename":{"first_name":"first","last_name":"last"}
    }
    collection.update_one({"_id":_id},updates)

update_person_by_id("65cf64079dc0071a18c5079f")


# Removing a document using id
def remove_person_by_id(person_id):
    _id=ObjectId(person_id)
    collection.update_one({"_id":_id},{"$unset":{"new_field":""}})

remove_person_by_id("65cf64079dc0071a18c5079f")

# Replacing one document
def replace_person_by_id(person_id):
    _id=ObjectId(person_id)
    a={
        "first_name":"Sample_name",
        "last_name":"backsample_name",
        "Age":30
    }
    collection.replace_one({"_id":_id},a)

replace_person_by_id("65cf64079dc0071a18c5079d")


# DELETING ONE DOCUMENT
def delete_doc_by_id(person_id):
    _id=ObjectId(person_id)
    collection.delete_one({"_id":_id})

delete_doc_by_id("65cf64079dc0071a18c5079b")

# DELETE MANY DOCUMENT
# def delete_many_doc_by_id(person_id):
#     _id=ObjectId(person_id)
#     collection.delete_many({})

# delete_many_doc_by_id("65cf64079dc0071a18c5079b")



#RELATION BETWEEN DIFFERENT COLLECTION(FOREIGN KEY..)
#  PRIMARY KEY OF MAIN WILL BE FOREIGN KEY OF OTHER COLLECTION