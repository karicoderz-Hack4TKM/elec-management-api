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

class MdmUsers(Resource):
    @auth.verifyToken
    def post(self, **tokenData):
        y = tokenData['userDetails']
        if y['userRole'] == current_app.config["RO_ADMIN"]:
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["users"]
                try:
                    data = request.get_json()
                    mydoc = selectCollection.find_one({"email": data["email"]})
                    # checking whether user is already present
                    if mydoc is None:
                        # encrypting password
                        data["password"] = str(uuid.uuid4().hex)
                        pwd = data["password"]

                        data["password"] = cipher.EncryptionService().encryptText(data["password"],
                                                                                  current_app.config["CIPHER_KEY"])
                        addOn = {"createdOn": datetime.now(), "updatedOn": datetime.now(), "_id": str(uuid.uuid4())}
                        data.update(addOn)
                        y = selectCollection.insert_one(data)
                        connect.close()

                        if y.inserted_id:


                            rec_email = data["email"]
                            Subject="Account Created - TKM Stock Register Suite"
                            name =data['username']
                            link = current_app.config["FORGOT"]
                            html1 = """<head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Login Email</title>
                            <link rel="preconnect" href="https://fonts.gstatic.com">
                            <link href="https://fonts.googleapis.com/css2?family=Courgette&display=swap" rel="stylesheet">
                            <style>
                            .container {
                                display: block;
                                border: 1px solid rgb(44, 44, 44);
                                margin-left: 100px;
                                margin-right: 100px;
                                color: #000;
                                font-weight: bold;
                                box-shadow: 25px 10px #888888;
                                background-color:#61DDEE ;
                               
                            }
                            .welcome-text {
                                font-size: 1.7em;
                                font-family: Callibri;
                            }
                            .card {
                                padding: 10px 30px;
                                display: block;
                                margin-left: auto;
                                margin-right: auto;
                                box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
                            }
                            .image {
                                margin: auto;
                            }
                            img {
                                display: block;
                                position: relative;
                                width: 100%;
                            }
                            
                            p {
                                font-size: 1.1em;
                            }
                            
                            .text {
                                font-weight: bold;
                                font-size: 2.0em;
                                text-align: center;
                            }
                            
                            .pass {
                                margin: 10px 30px;
                                padding: 10px;
                                word-wrap: break-word;
                                border: 2px solid grey;
                                background-color: #888888;
                            }
                            
                           .btn {
                                          position: absolute;
                                          top: 50%;
                                          left: 50%;
                                          transform: translate(-50%, -50%);
                                          -ms-transform: translate(-50%, -50%);
                                          background-color: #f1f1f1;
                                          color: black;
                                          font-size: 16px;
                                          padding: 16px 30px;
                                          border: none;
                                          cursor: pointer;
                                          border-radius: 5px;
                                          text-align: center;
                                        }
                                        
                                         .btn:hover {
                                          background-color: black;
                                          color: white;
                                        }
                                        .abtn
                                        {
                                        text-decoration:none;
                                        font-family: Times, "Times New Roman", Georgia, serif;
                                        }
                                        
                                        
                            
                           </style> 
                           </head>
                            <body>
                            <div class="container">
                            <div class="card">
                            <div class="image">
                            <img src="https://www.myfirstcollege.com/wp-content/uploads/2019/04/tkmce_logo.png" alt="logo">
                            </div>
                            <div class="col mt-4">
                            <h4 class=" fw-bold welcome-text">Welcome to TKM Stock Register </h4>
                            </div> """
                            html2  =   """<p>Hi <strong>"""
                            html3 = """,</strong></p>
                                        <p>
                                        You have been added to <strong>TKM Stock Register</strong> as <strong>Lab in Charge </strong>
                                        of <strong>"""
                            html4="""
                                  </strong>
                                  </p>
                                  <p>You may login to the software using the  change password link below </p>
                                  
                                   <a  class="abtn" href=
                                  """
                            html5 ="""
                                    target="_blank" "><button class="btn">CHANGHE PASSWORD </button></a>
                                  
                                    </div>
                                    </div> """
                            # HTML message

                            today = date.today()

                            html_content = html1  + str(today)+ html2+ name + html3 + html4 + link+ html5

                            response = emailservice.EmailSend().sendEmailWithHtml(subject=Subject,
                                                                                  reciever_email=rec_email,
                                                                                  html=html_content)

                            return {"code": 201, "message": f"{data['username']} is Successfully created"},201
                        else:
                            return {"code": 211, "message": f"{data['username']} is Not created"},211
                    else:
                        return {"code": 212, "message": f"{data['email']} already Present"},212
                except Exception as e:
                    return {"code": 213, "message": "User is not created: " + str(e)},213
            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210
        else:
            return {"code": 401, "message": "Unauthorised User"},401

    @auth.verifyToken
    def get(self, **tokenData):
        global addon2
        y = tokenData['userDetails']
        if y['userRole'] == current_app.config["RO_ADMIN"]:
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["users"]
                try:
                    data = request.args.get("filter")
                    if data:
                        data = json.loads(data)
                        item1 = selectCollection.find(data,{'password':0})
                        connect.close()
                        item2 = time.TimeConverter().isoJsonArrayToEpochJsonArray(item1)
                        return {"code": 200, "message": "Data served", "data": item2},200
                    else:
                        x = selectCollection.find({},{'password':0})
                        connect.close()
                        item3 = time.TimeConverter().isoJsonArrayToEpochJsonArray(x)
                        return {"code": 200, "message": "Data served", "data": item3},200

                except Exception as e:
                    return {"code": 212, "message": "Not found or bad request : " + str(e)},212
            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210
        else:
            return {"code": 401, "message": "Unauthorised User"},401

    @auth.verifyToken
    def delete(self, **tokenData):
        y = tokenData['userDetails']
        if y['userRole'] == current_app.config["RO_ADMIN"]:
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["users"]
                try:
                    data = request.args.get("filter")
                    data = json.loads(data)
                    mydoc = selectCollection.find(data)
                    if mydoc:
                        y = selectCollection.delete_one(data)
                        connect.close()
                        if y.deleted_count:
                            return {"code": 200, "message": "User Deleted"},200
                        else:
                            return {"code": 212, "message": "User Not Found"},212
                    else:
                        return {"code": 213, "message": "No User Available : "},213
                except Exception as e:
                    return {"code": 211, "message": "Not found or bad request : " + str(e)},211
            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210
        else:
            return {"code": 401, "message": "Unauthorised User"},401

    @auth.verifyToken
    def put(self, **tokenData):
        y = tokenData['userDetails']
        if y['userRole'] == current_app.config["RO_ADMIN"]:
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["users"]

                try:
                    data = request.get_json()
                    mydoc = selectCollection.find_one(data["_id"], {"_id": 0, 'password': 0, "createdOn": 0, "updatedOn": 0})
                    if mydoc:
                        newvalues = {"$set": data}
                        x = selectCollection.update_one(mydoc, newvalues)
                        mydoc = selectCollection.find_one(data["_id"],
                                                          {"_id": 0, 'password': 0, "createdOn": 0, "updatedOn": 0})
                        newvalues1 = {"$set": { "updatedOn": datetime.now()}}
                        y = selectCollection.update_one(mydoc, newvalues1)
                        connect.close()
                        if x.modified_count and y.modified_count:
                            return {"code": 200, "message": "User Data Updated"},200
                        else:
                            return {"code": 211, "message": "User Data Not Updated"},211
                    else:
                        return {"code": 212, "message": "User Not Found"},212

                except Exception as e:
                    return {"code": 213, "message": "Not found or bad request : " + str(e)},213

            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210
        else:
            return {"code": 401, "message": "Unauthorised User"},401