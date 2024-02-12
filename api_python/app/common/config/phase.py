from api_python.app.common.config.configuration import config


IS_PROD = config["general"]["phase"] == "prod"
IS_DEV = config["general"]["phase"] == "dev"
IS_LOCAL = config["general"]["phase"] == "local"
