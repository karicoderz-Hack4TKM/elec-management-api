from flask import current_app, request, render_template
from flask_restful import Resource
import pymongo
import common.auth.token_utils as auth
from datetime import datetime
import uuid
import json
import common.utils.time_conversion as time
import common.auth.encryption_service as cipher
import common.utils.email_service as emailservice
from datetime import date


class Send(Resource):
    def post(self):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["users"]
        except Exception as e:
            return e
        try:
            data = request.get_json()
            Subject = data["subject"]
            html1 = """<!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    <title>Alert Email</title>
                                </head>
                                <body>
                                <img src="https://drive.google.com/file/d/1KsDNzZeBxnLgIQM8hb96TrO1CEaqQ3aK/view?usp=drivesdk">
                                    <h3>"""

            html2 = """</h3>
                                    <p>"""
            html3 = """</p>
                                    </body>
                                    </html>"""

            today = date.today()
            html_content = html1 + str(today) + html2 + data["message"] + html3
            response = emailservice.EmailSend().sendEmailWithHtml(subject=Subject,reciever_email="ajohn3503@gmail.com",html=html_content)
            return {"code": 201, "message": "email  is sent Successfully "}, 201
        except Exception as e:
            return {"code": 213, "message": " not send: " + str(e)}, 213


