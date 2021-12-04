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

class Users(Resource):
    @auth.verifyToken
    def post(self, **tokenData):
        y = tokenData['userDetails']
        connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
        selectDb = connect[current_app.config["DB_NAME"]]
        selectCollection = selectDb["users"]
        try:
            data = request.get_json()
            pr = {
                "_id": "HD" + str(uuid.uuid4().hex),
                "email": data["email"],
                "password": data["password"],
                "lanenumber":data["lanenumber"] ,
                "usertype": data["usertype"]
            }
            UserInsert = selectCollection.insert_one(pr)
            connect.close()
            if UserInsert.inserted_id:
                return {"codee": 201, "message": f"{data['usertype']}  is Successfully Created "}, 201
            else:
                return {"code": 211, "message": "User is not inserted : "}, 401
        except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 500

    def get(self, **tokenData):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["users"]

            try:
                data = request.args.get("filter")
                if data is None:
                    x = list(selectCollection.find())
                    connect.close()
                    return {"code": 200, "message": "Data served", "data": x}, 200
                else:
                    data = json.loads(data)
                    mydoc = list(selectCollection.find(data))
                    connect.close()
                    return {"code": 200, "message": "Data served", "data": mydoc}, 200

            except Exception as e:
                    return {"code": 211, "message": "Not found or bad request : " + str(e)}, 211

        except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 210
