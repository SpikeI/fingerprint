from model import AllFeature, CrossFeature, RequestRecord, User, UserNetwork
from database import db
import json
import datetime
from app import app

def check_feature(uid, data):
    # check browser and device feature
    # todo :// finish
    result = {
        "status": True,
        "browser": False,
        "device": False
    }
    target_user = User.query.filter_by(id=uid).first()
    if not target_user:
        # user not found
        result['status'] = False
        return result

    try:
        target_allfeature = json.loads(target_user.feature)
    except Exception as e:
        print('[-] Error in json load {}'.format(e))
        result['status'] = False
        return result

    print(target_allfeature)
    for one_feature in target_allfeature:
        print("[+] Now check feature {}".format(one_feature))
        target_feature = AllFeature.query.filter_by(id=one_feature).first()
        if not target_feature:
            # No feature in user
            result['status'] = False
            return result

        # check browser feature
        if check_browser_feature(target_feature, data):
            result['browser'] = True
            return result

    for one_feature in target_allfeature:
        print("[+] Now check feature {}".format(one_feature))
        target_feature = AllFeature.query.filter_by(id=one_feature).first()
        # check device feature
        device_feature = CrossFeature.query.filter_by(id=target_feature.crossfeature).first()
        if not device_feature:
            result['status'] = False
            return result

        if check_device_feature(device_feature, data):
            insert_feature(uid, data)
            result['device'] = True
            return result

    return result

def check_browser_feature(feature, data):
    score = 0
    feature_score = app.config['BROWSER_FEATURE']
    percent = gen_percent(feature_score)

    for key in percent:
        if str(getattr(feature, key)) == str(data[key]):
            print("[+] Browser {} get score {}".format(key, percent[key]))
            score += percent[key]
        else:
            print("[-] Browser do not get {} score {}".format(key, percent[key]))
            print(type(getattr(feature, key)))
            print(type(data[key]))

    print("[+] Browser feature score is {}".format(score))
    if score > app.config['BROWSER_PASS']:
        return True
    else:
        return False

def check_device_feature(feature, data):
    score = 0
    feature_score = app.config['DEVICE_FEATURE']
    percent, device_test_percent = gen_percent(feature_score, app.config['CROSS_TEST_NUM'])

    # check webgltest
    cross_test = data['cross_fingerprint_test']

    for i in range(app.config['CROSS_TEST_NUM']):
        if getattr(feature, "webgl_test" + str(i + 1)) == cross_test[i]:
            score += device_test_percent

    for key in percent:
        if getattr(feature, key) == data[key]:
            score += percent[key]

    print("[+] Device feature score is {}".format(score))
    if score > app.config['DEVICE_PASS']:
        return True
    else:
        return False


def gen_percent(feature_score, device_test_num=None):
    total = 0
    percent = feature_score
    if not device_test_num:
        for key in feature_score:
            total += feature_score[key]

        for key in percent:
            percent[key] = (float(percent[key])/total) * 100

        return percent
    else:
        for key in feature_score:
            total += feature_score[key]

        device_test = app.config['DEVICE_TEST']
        total += device_test * device_test_num

        for key in percent:
            percent[key] = (float(percent[key])/total) * 100

        return percent, (device_test/total) * 100


def check_id(uid):
    # check if uid existed
    target = User.query.filter_by(id=uid).first()
    if target:
        return True
    else:
        return False

def store_info(uid, data, isnew=False, UserHandler=None, mark=""):
    # todo :// finish
    # store information in database
    # get cross features
    try:
        cross_features = data['cross_fingerprint_test']

        cf = CrossFeature()
        for i in range(app.config['CROSS_TEST_NUM']):
            setattr(cf, "webgl_test"+str(i+1), cross_features[i])
        cf.timezone = data['timezone']
        cf.fonts = data['fonts']
        cf.audio = data['audio']
        cf.cpu_cores = data['cpu_cores']
        cf.device_memory = data['device_memory']
        cf.navigator_platform = data['navigator_platform']

        db.session.add(cf)
        db.session.commit()
        # get browser features
        af = AllFeature(cf.id)
        af.is_webgl = data['WebGL']
        af.is_adblock = data['adBlock']
        af.is_cookie = data['cookie']
        af.is_localstorage = data['localstorage']
        af.canvas_test = data['canvas_test']
        af.font_list = data['fontlist']
        af.gpu = data['gpu']
        af.gpu_imgs = str(data['gpu_imgs'])
        af.hash = data['hash']
        af.inc = data['inc']
        af.manufacturer = data['manufacturer']
        af.plugins = data['plugins']
        af.video = str(data['video'])
        af.resolution = data['resolution']
        af.color_depth = data['color_depth']

        db.session.add(af)
        db.session.commit()

        rr = RequestRecord()
        rr.userid = uid
        rr.feature = af.id
        rr.req_time = datetime.datetime.now()

        db.session.add(rr)
        db.session.commit()

        if isnew:
            UserHandler.feature = json.dumps([af.id])
            UserHandler.localstorage = mark
            db.session.add(UserHandler)
            db.session.commit()

    except Exception as e:
        print("[-] Error in Storage {}".format(e))
        return False

    return True

def insert_feature(uid, data):
    target_user = User.query.filter_by(id=uid).first()
    if not target_user:
        return False

    try:
        cross_features = data['cross_fingerprint_test']

        cf = CrossFeature()
        cf.webgl_test1 = cross_features[0]
        cf.webgl_test2 = cross_features[1]
        cf.webgl_test3 = cross_features[2]
        cf.webgl_test4 = cross_features[3]
        cf.webgl_test5 = cross_features[4]
        cf.webgl_test6 = cross_features[5]
        cf.webgl_test7 = cross_features[6]
        cf.webgl_test8 = cross_features[7]
        cf.webgl_test9 = cross_features[8]
        cf.webgl_test10 = cross_features[9]
        cf.webgl_test11 = cross_features[10]
        cf.webgl_test12 = cross_features[11]
        cf.webgl_test13 = cross_features[12]
        cf.timezone = data['timezone']
        cf.fonts = data['fonts']
        cf.audio = data['audio']
        cf.cpu_cores = data['cpu_cores']
        cf.device_memory = data['device_memory']
        cf.navigator_platform = data['navigator_platform']

        db.session.add(cf)
        db.session.commit()
        # get browser features
        af = AllFeature(cf.id)
        af.is_webgl = data['WebGL']
        af.is_adblock = data['adBlock']
        af.is_cookie = data['cookie']
        af.is_localstorage = data['localstorage']
        af.canvas_test = data['canvas_test']
        af.font_list = data['fontlist']
        af.gpu = data['gpu']
        af.gpu_imgs = str(data['gpu_imgs'])
        af.hash = data['hash']
        af.inc = data['inc']
        af.manufacturer = data['manufacturer']
        af.plugins = data['plugins']
        af.video = str(data['video'])
        af.resolution = data['resolution']
        af.color_depth = data['color_depth']

        db.session.add(af)
        db.session.commit()

        rr = RequestRecord()
        rr.userid = uid
        rr.feature = af.id
        rr.req_time = datetime.datetime.now()

        db.session.add(rr)
        db.session.commit()

        target_user_feature = json.loads(target_user.feature)
        target_user_feature.append(af.id)
        target_user.feature = json.dumps(target_user_feature)
        db.session.add(target_user)
        db.session.commit()

        return True

    except Exception as e:
        print("[-] Error in insert {}".format(e))
        return False

    pass


def set_user_network(uid, data, remote_addr):
    try:
        target_user = User.query.filter_by(id=uid).first()
        new_network = UserNetwork()
        new_network.local = data['ipaddr']
        new_network.export = remote_addr
        db.session.add(new_network)
        db.session.commit()
        target_user.network = new_network.id
        db.session.add(target_user)
        db.session.commit()
        pass
    except Exception as e:
        print('[-] Error {}'.format(e))
        pass


def check_new_user(data):
    try:
        all_user = User.query.all()
        for one_user in all_user:
            print('[+] Now check {}'.format(one_user.id))
            result = check_feature(one_user.id, data)
            if result['status']:
                if result['browser']:
                    print('[+] found browser')
                    return one_user.id
                if result['device']:
                    return one_user.id
        return None
        pass
    except Exception as e:
        pass