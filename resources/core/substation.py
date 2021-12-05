from flask import current_app, request
from flask_restful import Resource
import pymongo
import common.auth.token_utils as auth
import numpy as np

import json
class Allview(Resource):
    def get(self):
        try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["users"]
                try:
                    agg_result = selectCollection.aggregate(
                        [{
                            "$group":
                                {"_id": "$usertype",
                                 "count": {"$sum": 1}
                                 }}
                        ])

                    data = [x for x in agg_result]
                    for i in range(len(data)):
                        doc = selectCollection.find_one({"usertype": data[i]["_id"]})
                        value = np.array(doc['12']).mean()
                        data[i]["average"] = value
                    return data

                except Exception as e:
                    return {"code": 212, "message": "Not found or bad request : " + str(e)}, 400
        except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 500