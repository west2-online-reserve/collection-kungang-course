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


train_bp = Blueprint('train-plan', __name__, url_prefix='/api')
from .database import get_db

system=get_db(config.DataBase_Name)

@train_bp.route('/training-plan', methods=['POST'])
@jwt_required()
def train_plan():
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

        data=request.json
        id=system.training_plan_manager.add_training_plan(user['id'],data['date'],data['project'],data['target'],data['note'])


        result={
            "id": id,
            "date": data['date'],
            "project": data['project'],
            "target": data['target'],
            "note": data['note'],
            "completed": False,
            "actualCount": 0
        }
        return success_response(message='创建成功',data=result)
    except Exception as e:
        return error_response(str(e), 500)


@train_bp.route('/training-plan/list',methods=['GET'])
@jwt_required()
def train_plan_list():
    try:
        user_id = get_jwt_identity()
        users = system.user_manager.get_all_users()
        user = None
        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break

        if not user:
            return error_response('用户不存在', 404)



        result=system.training_plan_manager.get_user_plans(user['id'])

        data={
            'list':result,
            'total':len(result)
        }
        return success_response(message='获取成功',data=data)
    except Exception as e:
        print(str(e))
        return error_response(str(e), 500)


@train_bp.route('/training-plan/<id>',methods=['PUT'])
@jwt_required()
def train_plan_update(id):
    try:
        user_id = get_jwt_identity()
        users = system.user_manager.get_all_users()
        user = None
        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break

        if not user:
            return error_response('用户不存在', 404)

        data=request.json
        target=data.get('target',None)
        note=data.get('note',None)
        actualCount=data.get('actualCount',None)
        completed=data.get('completed',None)

        bl=system.training_plan_manager.update_training_plan(id,user['id'],target,note,completed,actualCount)
        if bl:
            result=system.training_plan_manager.get_plan_by_id(id)
            return success_response(message='更新成功',data=result)
        else:
            return error_response('更新失败', 201)
    except Exception as e:
        print(str(e))
        return error_response(str(e), 500)


@train_bp.route('/training-plan/<id>',methods=['DELETE'])
@jwt_required()
def train_plan_delete(id):
    try:
        user_id = get_jwt_identity()
        users = system.user_manager.get_all_users()
        user = None
        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break

        if not user:
            return error_response('用户不存在', 404)

        if system.training_plan_manager.delete_training_plan(id,user['id']):
            return success_response(message='删除成功')
        else:
            return error_response('删除失败',201)
    except Exception as e:
        print(str(e))
        return error_response(str(e), 500)

@train_bp.route('/training-plan/trained-dates',methods=['GET'])
@jwt_required()
def train_plan_trained_dates():
    try:
        user_id = get_jwt_identity()
        users = system.user_manager.get_all_users()
        user = None
        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break
        if not user:
            return error_response('用户不存在', 404)

        year=request.args.get('year',None)
        month=request.args.get('month',None)

        print(year,month)
        result=system.training_plan_manager.get_trained_date(user['id'],year,month)
        result['date']=result['date']

        return success_response(message='获取成功',data=result)
    except Exception as e:
        print(str(e))
        return error_response(str(e), 500)
