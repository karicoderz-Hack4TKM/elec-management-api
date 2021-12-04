from flask import current_app, request,render_template
from flask_restful import Resource
import pymongo
import common.auth.token_utils as auth
from datetime import datetime
import uuid
import json
import common.utils.time_conversion as time
import common.auth.encryption_service as cipher
import  common.utils.email_service as emailservice
import smtplib
import imghdr
from  email.message import EmailMessage
from datetime import date

class Consumption(Resource):
    @auth.verifyToken
    def get(self, **tokenData):
        global addon2
        y = tokenData['userDetails']
        try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["consumption"]
                try:
                    data = request.args.get("filter")
                    if data:
                        data = json.loads(data)
                        item1 = selectCollection.find(data, {'_id': 0})
                        item2 = time.TimeConverter().isoJsonArrayToEpochJsonArray(item1)
                        # for i in item2:
                        #    hr=i["time"]
                        #     d=
                        #    d= datetime.utcfromtimestamp(3600 * (hr + 1800) // 3600))
                        #    print(d)
                        connect.close()
                        return {"code": 200, "message": "Data served", "data": item2}, 200

                    else:
                        x = selectCollection.find({}, {'_id': 0})
                        item3 = time.TimeConverter().isoJsonArrayToEpochJsonArray(x)
                        connect.close()


                        return {"code": 200, "message": "Data served", "data": item3}, 200
                except Exception as e:
                    return {"code": 212, "message": "Not found or bad request : " + str(e)}, 400
        except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 500

