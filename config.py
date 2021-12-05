from dotenv import load_dotenv
load_dotenv()

class Config(object):
    # MONGO_URL = "mongodb://localhost:27017/"
    MONGO_URL = "mongodb+srv://1012hackathon:1012tkmce@cluster0.9tsp4.mongodb.net"
    TOKEN_EXPIRY = 1000000
    DB_NAME = "hackthon"
    MAIL_TOKEN_EXPIRY = 15

    #encryption
    SECRET_KEY = "january"
    CIPHER_KEY="D4wJUp_ufSzUdparM11D4jD8VCWnw6G8SFcK6szO1uM="
    SECRET_KEY_FOR_EMAIL = "hai"

    #email config
    EMAIL_USERNAME = "elecmanagement123@gmail.com"
    EMAIL_PASSWORD = "Elec@123"

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
