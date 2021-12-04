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


class Excess(Resource):
    @auth.verifyToken
    def post(self, **tokenData):
        y = tokenData['userDetails']
        connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
        selectDb = connect[current_app.config["DB_NAME"]]
        selectCollection = selectDb["excess"]
        try:
            data = request.get_json()
            pr = {

                "type": data["type"],
                "reason": data["reason"],
                "userid":data["userid"],
                "start_date":time.TimeConverter.dateStringtoISOformat(self,data['start_date']),
                "end_date": time.TimeConverter.dateStringtoISOformat(self,data['end_date'])

            }
            UserInsert = selectCollection.insert_one(pr)
            connect.close()
            if UserInsert.inserted_id:
                return {"codee": 201, "message": f"{data['type']}  is Successfully Created "}, 201
            else:
                return {"code": 211, "message": "Excess request is not inserted : "}, 401
        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 500
