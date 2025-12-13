import datetime
import hashlib
import json
import os
import threading
import time
import uuid

import requests
from flask import Flask, request, jsonify, Blueprint, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.utils import secure_filename

from . import config

from .api.tools import error_response, success_response, hash_password


history_bp = Blueprint('history', __name__, url_prefix='/api')
from .database import get_db

system=get_db(config.DataBase_Name)


@history_bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    try:

        user_id = get_jwt_identity()

        # 通过ID获取用户信息
        users = system.user_manager.get_all_users()
        user = None

        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break
        if not user:
            return error_response('用户不存在', 404)


        historys=system.history_manager.get_history_by_user(user['id'])
        # print(historys)
        result=[]
        for history in historys:
            r={}
            r['id'] = int(history['id'])
            r['project'] = history['project']
            r['time'] = history['time'].strftime("%Y-%m-%d %H:%M:%S")
            r['score'] = int(history['score'])
            r['date'] =history['time'].strftime("%Y-%m-%d")
            result.append(r)

        # print(result)
        data={
            'data':result

        }
        return success_response(data,200)
    except Exception as ex:
        return error_response(str(ex), 500)

@history_bp.route('/history/detail/<id>', methods=['GET'])
@jwt_required()
def history_detail(id):
    try:
        user_id = get_jwt_identity()
        # 通过ID获取用户信息
        users = system.user_manager.get_all_users()
        user = None
        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break
        if not user:
            return error_response('用户不存在', 404)

        history = system.history_manager.get_history_records_by_id(int(id))[0]

        data={
            'project': history['project'],
            'time': history['time'].strftime("%Y-%m-%d %H:%M:%S"),
            'score': int(history['score']),
            'evaluation': history['content'],
        }

        return success_response(data, 200)
    except Exception as ex:
        return error_response(str(ex), 500)


