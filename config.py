class Config(object):
    SECRET_KEY = "imspikewhoyou"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/spike/paper/untitled/test.db'
    # name of cookie
    COOKIE_NAME = "FPID"
    BROWSER_FEATURE = {
        "canvas_test": 12,
        "gpu": 2,
        "gpu_imgs": 4,
        "hash": 5,
        "inc": 1,
        "plugins": 5,
        "resolution": 4,
        "video": 2,
        "color_depth": 1
    }
    BROWSER_PASS = 80
    DEVICE_TEST = 10
    DEVICE_FEATURE = {
        "fonts": 5,
        "timezone": 3,
        "audio": 10,
        "cpu_cores": 3,
        "device_memory": 2,
        "navigator_platform": 5
    }
    DEVICE_PASS = 80
    CROSS_TEST_NUM = 14
    FEATURE_NUM = 29
    INDEX_PAGE_SIZE = 10

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class Development(Config):
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True