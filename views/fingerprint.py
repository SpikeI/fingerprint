from flask import Blueprint, render_template, request, session
from database import db
from model import User
from utils import decrypt, encrypt
from views.fingerprint_util.utils import check_id, check_feature, store_info, insert_feature, set_user_network, check_new_user
import json, hashlib, time

fingerprint = Blueprint('fingerprint', __name__, template_folder='templates')


@fingerprint.route("/", methods=['GET', 'POST'])
def fingerprint_func():
    return render_template('fingerprint.html')


@fingerprint.route('/features', methods=['GET', 'POST'])
def get_features():
    # print(request.data)
    response = {}
    # print(request.data)
    data = json.loads(request.data)

    if "uid" in data:
        # get ID
        try:
            uid = int(decrypt(data['uid']))
        except:
            print("[-] Get ID failed")
            response['status'] = "failed"
            return json.dumps(response)

        if check_id(uid):
            # store feature
            # check if we got the right fingerprint
            check_result = check_feature(uid, data)
            target_user = User.query.filter_by(id=uid).first()
            if not target_user:
                response['status'] = "failed"
                return json.dumps(response)

            if check_result['browser']:
                # browser found
                print("[+] Browser fingerprint found !")
                target_user.check_browser += 1
                db.session.add(target_user)
                db.session.commit()
                response['status'] = "success"
                pass
            elif check_result['device']:
                # device found
                print("[+] device fingerprint found !")
                target_user.check_device += 1
                db.session.add(target_user)
                db.session.commit()
                response['status'] = "success"
                pass
            else:
                store_info(uid, data, isnew=False)
                response['status'] = "success"
                pass

            session['id'] = uid
            return json.dumps(response)
        else:
            # error
            response['status'] = 'failed'
            return json.dumps(response)
            pass

        pass
    else:
        # new user
        check_res = check_new_user(data)
        if check_res:
            response['status'] = "existed"
            response['uid'] = encrypt(str(check_res)).decode('utf-8')
            mark = User.query.filter_by(id=check_res).first().localstorage
            response['mark'] = mark

            return json.dumps(response)
        else:
            print("[-] No user checked")
        new_user = User()
        db.session.add(new_user)
        db.session.commit()

        session['id'] = new_user.id
        mark = hashlib.md5((str(new_user.id) + str(time.time())).encode('utf-8')).hexdigest()
        store_info(new_user.id, data, isnew=True, UserHandler=new_user, mark=mark)
        set_user_network(new_user.id, data, request.remote_addr)

        response['uid'] = encrypt(str(new_user.id)).decode('utf-8')
        response['status'] = "new"
        response['mark'] = mark
        print(response)

        return json.dumps(response)




@fingerprint.route("/check_storage", methods=["GET", "POST"])
def fingrtprint_check_storage():
    # todo : finish logic
    res = {}
    storage = set()
    for key in request.form:
        storage.add(request.form[key])

    flag = False
    mark = ""

    for item in storage:
        # check if item in database
        result = User.query.filter_by(localstorage=item).first()
        if result:
            flag = True
            session['id'] = result.id
            mark = item
            break

    if not flag:
        res['status'] = "unvalid"
    else:
        res['status'] = "valid"
        res['mark'] = mark

    return json.dumps(res)


