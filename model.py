from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from database import db


class CrossFeature(db.Model):
    __tablename__ = 'CrossFeature'
    id = Column(Integer, primary_key=True)
    webgl_test1 = Column(String(40), default="")
    webgl_test2 = Column(String(40), default="")
    webgl_test3 = Column(String(40), default="")
    webgl_test4 = Column(String(40), default="")
    webgl_test5 = Column(String(40), default="")
    webgl_test6 = Column(String(40), default="")
    webgl_test7 = Column(String(40), default="")
    webgl_test8 = Column(String(40), default="")
    webgl_test9 = Column(String(40), default="")
    webgl_test10 = Column(String(40), default="")
    webgl_test11 = Column(String(40), default="")
    webgl_test12 = Column(String(40), default="")
    webgl_test13 = Column(String(40), default="")
    webgl_test14 = Column(String(40), default="")
    webgl_test_expand1 = Column(String(40), default="")
    webgl_test_expand2 = Column(String(40), default="")
    webgl_test_expand3 = Column(String(40), default="")
    timezone = Column(Integer, default=0)
    fonts = Column(String(2048), default="")
    audio = Column(String(256), default="")
    cpu_cores = Column(Integer, default=0)
    # get from fingerprintjs
    device_memory = Column(Integer, default=0)
    navigator_platform = Column(String(512), default="")


    def __init__(self):
        pass

    def __repr__(self):
        return '<Cross Feature %d>' % (self.id)


class AllFeature(db.Model):
    __tablename__ = 'AllFeature'
    id = Column(Integer, primary_key=True)
    crossfeature = Column(Integer, db.ForeignKey('CrossFeature.id'))
    is_webgl = Column(Boolean, default=False)
    is_adblock = Column(String(10), default="")
    is_cookie = Column(Boolean, default=False)
    is_localstorage = Column(Boolean, default=False)
    canvas_test = Column(String(40), default="")
    font_list = Column(String(1024), default="")
    gpu = Column(String(256), default="")
    gpu_imgs = Column(String(512), default="")
    hash = Column(Integer, default=0)
    inc = Column(String(256), default="")
    manufacturer = Column(String(1024), default="")
    plugins = Column(String(1024), default="")
    resolution = Column(String(256), default="")
    video = Column(String(1024), default="")
    # get from fingerprintJS
    color_depth = Column(Integer, default=0)


    def __init__(self, crossfeature):
        self.crossfeature = crossfeature
        pass

    def __repr__(self):
        return "<All feature %d>" % (self.id)


class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    feature = Column(String(1024), default='[]')
    network = Column(String(2048), default='')
    check_storage = Column(Integer, default=0)
    check_browser = Column(Integer, default=0)
    check_device = Column(Integer, default=0)
    localstorage = Column(String(128), default=None)

    def __init__(self):
        pass


class RequestRecord(db.Model):
    __tablename__ = "RequestRecord"
    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    feature = Column(Integer, db.ForeignKey("AllFeature.id"), default=None)
    req_time = Column(DateTime, default=None)

    def __init__(self):
        pass


class ResearchPanel(db.Model):
    __tablename__ = "ResearchPanel"
    id = Column(Integer, primary_key=True)
    total_request = Column(Integer, default=0)
    right_confirm = Column(Integer, default=0)
    wrong_confirm = Column(Integer, default=0)
    fingerprint_request = Column(Integer, default=0)
    right_fingerprint = Column(Integer, default=0)
    wront_fingerprint = Column(Integer, default=0)


class UserNetwork(db.Model):
    __tablename__ = "UserNetwork"
    id = Column(Integer, primary_key=True)
    export = Column(String(256), default="")
    local = Column(String(256), default="")

    def __init__(self):
        pass