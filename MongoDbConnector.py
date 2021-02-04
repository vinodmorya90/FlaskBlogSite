from pymongo import MongoClient
import bson
import datetime


class MongoDbConnector:

    def __init__(self, ConnectionUrl: str, dbName: str):
        client = MongoClient(ConnectionUrl)
        self.db = client[dbName]

    def listTables(self) -> str:
        return self.db.list_collection_names()

    def insertIntoTable(self, tableName: str, collection: dict):
        table = self.db[tableName]
        table.insert_one(collection)

    def UpdateSingleRecordInTable(self, tableName: str, idInString: str, collection: dict):
        id = bson.ObjectId(idInString)
        table = self.db[tableName]
        updateQuery= {"$set":collection}
        table.update_one({"_id": id}, updateQuery)

    def GetSingleRecord(self, tableName: str, idInString: str) -> dict:
        id = bson.ObjectId(idInString)
        table = self.db[tableName]
        return table.find_one(id)

    def GetAllRecords(self, tableName: str, filterParameters: dict = {}) -> list:
        table = self.db[tableName]
        return table.find(filterParameters)

    def DeleteItem(self,tableName:str,idInString: str):
        id = bson.ObjectId(idInString)
        table=self.db[tableName]
        table.delete_one({'_id':id})

if __name__ == '__main__':
    mongoDb = MongoDbConnector("mongodb+srv://sa:admin@cluster0.c2wxg.mongodb.net/vikalp?retryWrites=true&w=majority",
                               "vikalp")

    # 1. print all tables
    print(mongoDb.listTables())

    # 2. insert statement
    post = {"author": "Surendra", "text": "first connection to mongo", "tags": ["vikalp", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}
    mongoDb.insertIntoTable("posts", post)

    # 3. update query
    updateQuery = {"$set": {"text": "Canyon ", "asd": "qwert"}}
    mongoDb.UpdateSingleRecordInTable("posts", "60155f2e1ac3e4539146e969", updateQuery)

    # 4. using Id
    print(mongoDb.GetSingleRecord("posts", "6015679cc989c35e8e0ffd96"))

    # 5. using filters
    for post in mongoDb.GetAllRecords("posts", {'author': 'Mike'}):
        print(post)

    print("Done")











