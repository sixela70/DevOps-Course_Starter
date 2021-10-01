import os
import pymongo
import datetime
from bson import ObjectId
from todo_app.data.item import Item
from todo_app.data.user import User

class MongoDb:

    init = False
    client = None
    database = None
    items_collection = None

    @classmethod
    def initdb(cls): 

        user=os.getenv('MONGO_USER')
        if not user:
            raise ValueError("No MONGO_USER set for application. Please check the enviroment")
        password=os.getenv('MONGO_USER_PW')
        if not password:
            raise ValueError("No MONGO_USER_PW set for application. Please check the enviroment")
        connection=os.getenv('MONGO_CONNECTION')
        if not connection:
            raise ValueError("No MONGO_CONNECTION set for application. Please check the enviroment")
        server=os.getenv('MONGO_SERVER')
        if not server:
            raise ValueError("No MONGO_SERVER set for application. Please check the enviroment")
        database=os.getenv('MONGO_DATABASE')
        if not database:
            raise ValueError("No MONGO_DATABASE set for application. Please check the enviroment")

        cls.client = pymongo.MongoClient(f"{connection}://{user}:{password}@{server}/{database}?w=majority", ssl=True, tlsAllowInvalidCertificates=True)
        print(f"Connected to {server}/{database}")
        cls.database=cls.client[database]
        cls.items_collection = cls.database.items_collection
        cls.user_collection = cls.database.users
        cls.init=True

    @classmethod
    def get_user(cls, username):
        if cls.init == False:
            cls.initdb()
        user = cls.user_collection.find_one({'username': username})
        if user == None:
            print(f"User not found {username}")
        else:
            return User(user['_id'], user['username'], user['role'])

    @classmethod
    def add_user(cls, username, role):
        if cls.init == False:
            cls.initdb()

        new_user = {"username": username, "role" : role}
        id = cls.user_collection.insert_one(new_user).inserted_id
        return  User(id,username, role)

    @classmethod
    def get_all_users(cls):
        if cls.init == False:
            cls.initdb()
        users = []
        print("Getting the users from the mongo db")
    
        user_objects = cls.user_collection.find({})
        for user_object in user_objects:
            user = User(user_object["_id"],user_object["username"], user_object["role"])

            users.append(user)

        return users


    """ Gets all the todo items from DB"""
    @classmethod
    def get_all_items(cls):
        if cls.init == False:
            cls.initdb()
        item_list = []
        items = cls.items_collection.find({})
        for item in items:
            item_object = Item(item["_id"],item["title"], item["status"], item["dateLastActivity"])
            item_list.append(item_object)

        return item_list

    @classmethod
    def update_item(cls, id, status):
        filter = { "_id": ObjectId(id) }
        newstatus = { "$set": { "status": status, "dateLastActivity": datetime.datetime.utcnow()} }
        cls.items_collection.update_one(filter, newstatus)

    @classmethod
    def markid_item_doing(cls,id):
        cls.update_item(id, "Doing")

    @classmethod
    def markid_item_done(cls,id):
        cls.update_item(id, "Done")

    ## Move item to the other list 
    @classmethod
    def mark_item_done(cls,item):
        cls.markid_item_done(item['id'])

    @classmethod
    def mark_item_not_done(cls,item):
        cls.markid_item_undone(item['id'])

    @classmethod    
    def markid_item_undone(cls,id):
        cls.update_item(id, "ToDo")

    @classmethod    
    def add_item(cls, title):
        item = {"title": title, 
                "status": "ToDo",
                "dateLastActivity": datetime.datetime.utcnow()}
        
        id = cls.items_collection.insert_one(item).inserted_id
        return id