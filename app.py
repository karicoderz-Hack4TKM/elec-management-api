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
import resources.core.user_roles as user_role
api.add_resource(user_role.MdmUserRoles,'/core/userRoles')

#users
import resources.core.users as user
api.add_resource(user.Users,'/core/users')

import resources.core.tariff as tariff
api.add_resource(tariff.Tariff,'/core/tariff')

#consumption
import resources.core.consumption as consumption
api.add_resource(consumption.Consumption,'/core/consumption')

#generators
import resources.core.generator as generator
api.add_resource(generator.Produce , '/core/generator')

#production
import resources.core.production as production
api.add_resource(production.Production,'/core/production')

#excess
import resources.core.execess as excess
api.add_resource(excess.Excess,'/core/excess')

#providers
import resources.core.providers as providers
api.add_resource(providers.Providers,'/core/providers')

#predictor
import resources.core.predictor1 as predict
api.add_resource(predict.LaneAverage,'/core/predict')

#electric_vehicle
import resources.core.electricvehicle as electricvehicle
api.add_resource(electricvehicle.ElectricVehicle,'/core/electricvehicle')


#bill
import resources.core.bill as bill
api.add_resource(bill.Bill,'/core/bill')

#allvalue
import resources.core.substation as substation
api.add_resource(substation.Allview,'/core/allview')

if __name__ == '__main__':
    app.run()