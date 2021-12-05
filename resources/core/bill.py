from flask import current_app, request,render_template
from flask_restful import Resource
import pymongo
import common.auth.token_utils as auth
import json
class Bill(Resource):
    @auth.verifyToken
    def get(self, **tokenData):
        try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["consumption"]
                try:
                    data = request.args.get("filter")
                    if data:
                        data = json.loads(data)
                        x = list(selectCollection.find(data))
                        total=0
                        for  data in x:
                            total=total+data["consumption"]

                        connect.close()
                        return {"code": 200, "message": "Data served","data":total}, 200

                except Exception as e:
                    return {"code": 212, "message": "Not found or bad request : " + str(e)}, 400
        except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 500