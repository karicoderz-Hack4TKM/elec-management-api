from dotenv import load_dotenv
load_dotenv()

class Config(object):
    #MONGO_URL = "mongodb://localhost:27017/"
    MONGO_URL = "mongodb+srv://1012hackathon:1012tkmce@cluster0.9tsp4.mongodb.net"
    TOKEN_EXPIRY = 1000
    DB_NAME = "hackathon"
    MAIL_TOKEN_EXPIRY = 15

    #encryption
    SECRET_KEY = "january"
    CIPHER_KEY="D4wJUp_ufSzUdparM11D4jD8VCWnw6G8SFcK6szO1uM="
    SECRET_KEY_FOR_EMAIL = "hai"

    #email config
    EMAIL_USERNAME = "tkmstockmanagement@gmail.com"
    EMAIL_PASSWORD = "tkmce1234"

    #user roles
    RO_ADMIN = "RO100"
    RO_LAB_IN_CHARGE = "RO101"

    #reset page url
    RESET_URL = "http://localhost:4200/reset?token="
    FORGOT ="http://localhost:4200/forgot"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class StagingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    MONGO_URL = "mongodb://root:example@mongo:27017"
    DEBUG = False
    TESTING = False

# other flask enironment variables
# FLASK_ENV - Controls the environment.
# FLASK_DEBUG - Enables debug mode.
# FLASK_RUN_EXTRA_FILES - A list of files that will be watched by the reloader in addition to the Python modules.
# FLASK_RUN_HOST - The host you want to bind your app to.
# FLASK_RUN_PORT - The port you want to use.
# FLASK_RUN_CERT - A certificate file for so your app can be run with HTTPS.
# FLASK_RUN_KEY - The key file for your cert.

# .env reference
# https://prettyprinted.com/tutorials/automatically_load_environment_variables_in_flask

