from flask import current_app,Response,request
from flask_restful import Resource
import pymongo
import json
import common.auth.token_utils as auth
from datetime import datetime, timedelta


class Produce(Resource):
    def put(self, **tokenData):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["generator"]
            try:
                data = request.get_json()
                mydoc = selectCollection.find_one(data["_id"])
                if mydoc:
                    newvalues = {"$set": data}
                    x=selectCollection.update_one(mydoc, newvalues)
                if x.modified_count:
                    print(1)
                    return {"code": 201, "message": "Generator Successfully Started"},201
            except Exception as e:
                return {"code": 211, "message": "Generator not Started : " + str(e)},211
        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210

    @auth.verifyToken
    def get(self, **tokenData):
        y = tokenData['userDetails']
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["generator"]
            try:
                data = request.args.get("filter")
                if data is None:
                    x = list(selectCollection.find())
                    connect.close()
                    return {"code": 200, "message": "Data served", "data": x},200

                else:
                    data = json.loads(data)
                    mydoc = list(selectCollection.find(data))
                    connect.close()
                    return {"code":200, "message": "Data served", "data": mydoc},200

            except Exception as e:
                return {"code": 211, "message": "Not found or bad request : " + str(e)},211

        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210
