import pymongo
import dns


class MongoManager:
    __instance = None

    @staticmethod
    def getInstance():
        if MongoManager.__instance == None:
            MongoManager()
        return MongoManager.__instance

    def __init__(self):
        if MongoManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoManager.__instance = pymongo.MongoClient(
                "mongodb+srv://admin:HADES2121@loteria-1egci.mongodb.net/test?retryWrites=true&w=majority")
