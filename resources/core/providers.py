from flask import current_app, request,render_template
from flask_restful import Resource
import pymongo
import common.auth.token_utils as auth
from datetime import datetime
import common.auth.encryption_service as cipher
import json
import jwt
import datetime

class Providers(Resource):
    def post(self):
        request_data = request.get_json()
        email = request_data["email"]
        password = request_data["password"]

        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["providers"]
            requiredUserData = selectCollection.find_one({"email": email})
            connect.close()

            if (requiredUserData != None):

                # decrpting password from db
                try:
                    decPassword = cipher.EncryptionService().decryptText(requiredUserData["password"],
                                                                         current_app.config["CIPHER_KEY"])
                except Exception as e:
                    return {"code": "213", "message": "Password Decryption Failure " + str(e)}

                if decPassword == password:
                    data = requiredUserData
                    pr = {
                        "_id": data["_id"],
                        "email": data["email"],
                        "password": data["password"],
                        "usertype": data["usertype"]
                    }

                    token = jwt.encode({"data": pr, 'exp': datetime.datetime.utcnow() + datetime.timedelta(
                        minutes=current_app.config["TOKEN_EXPIRY"])}, current_app.config["SECRET_KEY"])
                    return {"code": "200", "message": "Congrats! Access granted", "token": token, "data": pr}
                else:
                    return {"code": "211", "message": "Incorrect Password!"}
            else:
                return {"code": "212", "message": "User not found!"}

        except Exception as e:
            return {"code": "210", "message": "Failed to connect to Mongo DB : " + str(e)}

    @auth.verifyToken
    def get(self, **tokenData):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["providers"]

            try:
                data = request.args.get("filter")
                if data is None:
                    x = list(selectCollection.find({},{"_id":0}))
                    connect.close()
                    return {"code": 200, "message": "Data served", "data": x}, 200
                else:
                    data = json.loads(data)
                    mydoc = list(selectCollection.find(data,{"_id":0}))
                    connect.close()
                    return {"code": 200, "message": "Data served", "data": mydoc}, 200

            except Exception as e:
                return {"code": 211, "message": "Not found or bad request : " + str(e)}, 400

        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 500