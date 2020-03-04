import configparser
import os


class ConfigReader(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_config(self, section, option):
        config = configparser.ConfigParser()
        BASE_DIR = os.path.dirname(__file__)
        config_file = os.path.join(BASE_DIR, self.file_name)
        config.read(config_file, encoding='utf-8')
        res = config.get(section=section, option=option)
        return res


class Config(ConfigReader):
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'

    def __init__(self):
        super().__init__("config.ini")
        read_config = self.read_config
        self.MONGO_USER = read_config("DB_SETTING", "USER_DB")
        self.MONGO_PASS = read_config("DB_SETTING", "PASSWORD")
        self.MONGO_HOST = read_config("DB_SETTING", "HOST")
        self.MONGO_PORT = read_config("DB_SETTING", "PORT")
        self.INSTALLATION = read_config("INSTALLATION", "TYPE")
        self.MAIL_SERVER = read_config("MAIL", "MAIL_SERVER")
        self.MAIL_PORT = read_config("MAIL", "MAIL_PORT")
        self.MAIL_CHECK = read_config("MAIL", "MAIL_CHECK")
        self.SERVER_HOST = read_config("INSTALLATION", "HOST")
        self.SERVER_PORT = read_config("INSTALLATION", "PORT")


class Setup(Config):
    def __init__(self):
        super().__init__()
        self.mail_host_name = os.environ.get("MAIL_SERVER", self.MAIL_SERVER)
        self.mail_port = os.environ.get("MAIL_PORT", self.MAIL_PORT)
        self.mail_check = os.environ.get("MAIL_CHECK", self.MAIL_CHECK)

        mongo_host = os.environ.get("MONGODB_HOSTNAME", self.MONGO_HOST)
        mongo_port = os.environ.get("MONGODB_PORT", self.MONGO_PORT)
        mongo_user = os.environ.get("MONGODB_USER", self.MONGO_USER)
        mongo_password = os.environ.get("MONGODB_PASS", self.MONGO_PASS)

        account = f"{mongo_user}:{mongo_password}@" if mongo_user else ""
        self.mongo_url = f'mongodb://{account}{mongo_host}:{mongo_port}'

        self.server_port = os.environ.get("SERVER_PORT", self.SERVER_PORT)
        self.server_host = os.environ.get("SERVER_HOST", self.SERVER_HOST)