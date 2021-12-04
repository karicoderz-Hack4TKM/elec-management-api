from flask import current_app
from flask_restful import Resource, request
import jwt
import datetime
import pymongo
import common.auth.encryption_service as cipher
import common.utils.email_service as emailService
import common.auth.token_utils as auth


class UserLogin(Resource):
    def post(self):
        request_data = request.get_json()
        email = request_data["email"]
        password = request_data["password"]

        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["users"]
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
                        "lanenumber": data["lanenumber"],
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


class ForgotUserPassword(Resource):
    def post(self):
        request_data = request.get_json()
        userEmail = request_data["email"]
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["users"]
            requiredUserData = selectCollection.find_one({"email": userEmail})
            connect.close()
            if (requiredUserData != None):

                try:
                    name = requiredUserData["username"]
                    data = {"email": userEmail}
                    token = jwt.encode({"data": data, 'exp': datetime.datetime.utcnow() + datetime.timedelta(
                        minutes=current_app.config["MAIL_TOKEN_EXPIRY"])}, current_app.config["SECRET_KEY_FOR_EMAIL"])
                    link = current_app.config["RESET_URL"] + token
                    html1 = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>RESET PASSWORD</title>
                    
                    <style>
                   .button {
                    background: rgb(252, 2, 2);
                    border: 2px solid rgb(255, 255, 255);
                    padding: 10px 20px;
                    border-radius: 7px;
                    color: rgb(255, 255, 255);
                    display: block;
                    font-size: 1em;
                    font-weight: bold;
                    margin-left: 15PX;
                    padding: 10px 10px;
                    width: max-content;
                    position: relative;
                    text-transform: uppercase;
                    text-decoration: none;}
                    </style>
                    </head>
                    
                    <body>
                    <div style="display: block;background: #00abb7;
                    margin: 15px 30px;">
                    
                    <div style="padding: 10px 30px;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;">
                    
                    <div style="width:80%;
                    margin: 5px auto;">
                    
                    <img style="display: block;
                     position: relative;
                     width: 100%;" src="https://tkmce.ac.in/images/logo/header.png" alt="logo">
                   </div>
                    <div>
                    
                    <h4 style=" font-size:1.7em">Greetings from TKM Stock Register Suite</h4>
                     </div>
                     <p>Hi <strong>"""

                    html2 = """
                    </strong></p>
                    <p>
                    To reset your Password for <strong>TKM Stock Register Suite, </strong> please <strong>Click on Reset Password </strong>
                    </p>
                     <a class="button" href="""

                    html3 = """  
                    target="_blank" style="color: rgb(255, 255, 255);"> RESET PASSWORD</a>
                    <p>This link will expire in 15 minutes, so be sure to use it right away</p>
                    <p>Have a Good Day</p>
                    <p><em> This is a Electronically Generated Email Please Don't Reply</em></p><br><br>
                    </div>
                    </div>
                   </body>
                   </html>
                    """
                    # HTML message
                    html_content = html1 + name + html2 + link + html3
                    response = emailService.EmailSend().sendEmailWithHtml(subject="Reset Password", reciever_email=userEmail, html=html_content)
                    if(response[1]==200):
                        return {"code": 200, "message": "Recovery email sent successfully! Please check your Inbox."},200
                    else:
                        return response
                except:
                    return {"code": 421, "message": "Sorry! email recovery service failed."},421
            else:
                return {"code": 211, "message": "Sorry! This email is not valid."},211

        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210

class PasswordReset(Resource):
    @auth.verifyTokenForEmail
    def put(self, **tokenData):
        y = tokenData['userDetails']
        if y["email"]:
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["users"]

                try:
                    data = request.get_json()
                    mydoc = selectCollection.find_one({"_id": data["_id"]}, {"createdOn": 0})
                    if mydoc:
                        from datetime import datetime

                        encPassword = cipher.EncryptionService().encryptText(data["password"],current_app.config["CIPHER_KEY"])

                        newvalues = {"$set": {'password': encPassword, "updatedOn": datetime.now()}}
                        x = selectCollection.update_one(mydoc, newvalues)
                        connect.close()
                        if x.modified_count:
                            return {"code": 200, "message": "User Password Updated"}, 200
                        else:
                            return {"code": 211, "message": "User Password Not Updated"}, 211
                    else:
                        return {"code": 212, "message": "User Not Found"}, 212

                except Exception as e:
                    return {"code": 213, "message": "Not found or bad request : " + str(e)}, 213

            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 210
        else:
            return {"code": 401, "message": "Unauthorised User"}, 401

    @auth.verifyTokenForEmail
    def get(self, **tokenData):
        y = tokenData['userDetails']
        if y["email"]:
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["users"]
                try:
                    mydoc = selectCollection.find_one({"email": y["email"]}, {'password': 0})
                    if mydoc:
                        return {"code": 200, "message": " Valid User", "_id": mydoc["_id"]},200
                    else:
                        return {"code": 403, "message": "Not a valid User"}, 403
                except Exception as e:
                    return {"code": 211, "message": "Not found or bad request : " + str(e)},211

            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210
        else:
            return {"code": 401, "message": "Unauthorised User"},401