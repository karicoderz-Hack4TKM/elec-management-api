from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "staging":
    app.config.from_object("config.StagingConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")


### swagger specific ###
SWAGGER_URL = '/swagger-ui'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "TKM Stock Register API - Swagger UI"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


#Authorization APIs
import resources.authorization.login as authorization
api.add_resource(authorization.UserLogin,"/userLogin")
api.add_resource(authorization.ForgotUserPassword,"/forgotPassword")
api.add_resource(authorization.PasswordReset, "/resetPassword")






#userrole
import resources.mdm.user_roles as user_role
api.add_resource(user_role.MdmUserRoles,'/mdm/userRoles')

#users
import resources.mdm.users as user
api.add_resource(user.MdmUsers,'/mdm/users')





if __name__ == '__main__':
    app.run()