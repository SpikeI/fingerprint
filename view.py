from flask import render_template, session, redirect, url_for, request
from database import db
from app import app
from model import User, AllFeature, CrossFeature, UserNetwork
from decorator import login_required
from utils import encrypt, get_user_num, get_user_data
from utils import *
import json
from app import app

@app.route('/')
def index():
    return redirect(url_for("service"))
    # return render_template('index.html')

@app.route('/dbinit')
def db_init():
    db.create_all()
    return "OK"


@app.route('/service', methods=["GET", "POST"])
@login_required
def service():
    uid = encrypt(str(session['id'])).decode('utf-8')
    return render_template("service.html", uid=uid)

@app.route("/spikeadmin", methods=['GET', 'POST'])
def admin():
    feature_num = app.config['FEATURE_NUM']
    user_num = get_user_num()
    user_data = get_user_data(1)
    return render_template("index.html", feature_num=feature_num,
                           user_data=user_data, user_num=user_num)

@app.route("/spikeuser", methods=['GET', 'POST'])
def admin_user():
    if "id" not in request.args:
        return redirect(url_for('admin'))
    else:
        user_data = User.query.filter_by(id=int(request.args['id'])).first()
        if user_data:
            network_data = UserNetwork.query.filter_by(id=user_data.network).first()
            all_features = json.loads(user_data.feature)
            feature_list = []
            for one_feature in all_features:
                feature_data = AllFeature.query.filter_by(id=one_feature).first()
                if feature_data:
                    cross_data = CrossFeature.query.filter_by(id=feature_data.crossfeature).first()
                    if cross_data:
                        feature_list.append({
                            "browser": feature_data,
                            "cross": cross_data
                        })
                    else:
                        feature_list.append({
                            "browser": feature_data,
                            "cross": None
                        })
            if feature_list != []:
                return render_template("user.html", user_data=user_data, network_data=network_data,
                                           feature_list=feature_list)
            else:
                return render_template("user.html", user_data=None, network_data=network_data,
                                           feature_list=None)
        else:
            # redirect(url_for("admin"))
            return render_template("user.html", user_data=None, network_data=None,
                                   feature_data=None, cross_data=None)

@app.route('/spike', methods=['GET'])
def spike():
    return render_template("test.html")


@app.route("/test", methods=['GET'])
def test():
    # return
    # print(app.config['SECRET_KEY'])
    a = User.query.first()
    print(a.keys())
    return decrypt("MV0kD+C8uyP7epPyeKAb+KJOW64qhCUGaZuGI8RQBbQ=")

