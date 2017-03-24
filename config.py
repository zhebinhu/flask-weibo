import os

basedir = os.path.dirname(__file__)

def get_env_variable(var_name, default=False):
    """
    Get the environment variable or return exception
    :param var_name: Environment Variable to lookup
    """
    try:
        return os.environ[var_name]
    except KeyError:
        import StringIO
        import ConfigParser
        env_file = os.environ.get('PROJECT_ENV_FILE',basedir+"/.env")
        try:
            config = StringIO.StringIO()
            config.write("[DATA]\n")
            config.write(open(env_file).read())
            config.seek(0, os.SEEK_SET)
            cp = ConfigParser.ConfigParser()
            cp.readfp(config)
            value = dict(cp.items('DATA'))[var_name.lower()]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            os.environ.setdefault(var_name, value)
            return value
        except (KeyError, IOError):
            if default is not False:
                return default
            error_msg = "Either set the env variable '{var}' or place it in your " \
                        "{env_file} file as '{var} = VALUE'"
            print error_msg.format(var=var_name, env_file=env_file)


class Config:
    SECRET_KEY = get_env_variable('SECRET_KEY') or 'CKfQYF74QAssMz4X'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BLOG_MAIL_SUBJECT_PREFIX = '[Huzb]'
    BLOG_MAIL_SENDER = get_env_variable('BLOG_MAIL_SENDER')
    BLOG_ADMIN = get_env_variable('BLOG_ADMIN')
    BLOG_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    #DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = get_env_variable('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_variable('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = get_env_variable('DEV_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = get_env_variable('TEST_SQLALCHEMY_DATABASE_URI')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_env_variable('SQLALCHEMY_DATABASE_URI')

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}