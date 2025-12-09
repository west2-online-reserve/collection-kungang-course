import datetime
import hashlib
import json
import os
import threading
import time
import uuid

import numpy as np
import requests
from PIL import Image
from flask import Flask, request, jsonify, Blueprint, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.utils import secure_filename

from . import config
from .api.tools import error_response, success_response
from moviepy import VideoFileClip

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
from .database import get_db

system=get_db(config.DataBase_Name)
def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def get_video_duration(file_path):
    """获取视频时长（需要安装moviepy或opencv）"""
    try:
        # 方法1: 使用moviepy（推荐）

        with VideoFileClip(file_path) as video:
            return video.duration

    except Exception as e:
        return 0


def extract_first_frame_moviepy(video_path, thumbnail_path=None, size=(320, 180)):
    """
    使用moviepy提取视频第一帧

    Args:
        video_path: 视频文件路径
        thumbnail_path: 缩略图保存路径
        size: 缩略图尺寸 (宽, 高)

    Returns:
        str: 缩略图保存路径
    """
    try:
        # 打开视频文件
        with VideoFileClip(video_path) as video:

            # 获取第一帧
            frame = video.get_frame(0)  # 0表示第一秒的第一帧

            # 转换为PIL Image
            pil_image = Image.fromarray((frame * 255).astype(np.uint8))

            print(pil_image.size)

            # 调整大小
            pil_image.thumbnail(size, Image.Resampling.LANCZOS)

            if thumbnail_path:
                pil_image.save(thumbnail_path,  quality=85)
                return thumbnail_path
            else:
                return pil_image

    except Exception as e:
        print(e)
        return ''

@admin_bp.route('/media/upload', methods=['POST'])
@jwt_required()
def upload():
    try:
        user_id = get_jwt_identity()

        # 通过ID获取用户信息
        users = system.user_manager.get_all_users()
        user = None
        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break

        # print(user['role'])
        if not user:
            return error_response('用户不存在', 404)
        if user['role'] != 'admin':
            return error_response('权限不足', 405)

        if 'multipart/form-data' not in request.content_type:
            return error_response('请求类型必须是 multipart/form-data',400)

        name = request.form.get('name')
        annotation = request.form.get('annotation', '')
        file = request.files.get('file')

        if not name:
            return error_response('视频名称不能为空',400)

        if not file:
            return error_response('未提供视频文件',400)

        if not allowed_file(file.filename):
            return error_response(f'不支持的文件类型。允许的类型: {", ".join(config.ALLOWED_EXTENSIONS)}',400)

        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()

        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}"

        # 7. 保存文件
        save_path = os.path.join(config.VIDEO_FOLDER, unique_filename+f'.{file_extension}')
        thumbnail_path = os.path.join(config.THUMBNAIL_FOLDER, unique_filename+f'.jpg')
        file.save(save_path)
        # print(save_path)


        # 获取文件大小
        file_size = os.path.getsize(save_path)

        # 8. 获取视频信息（如时长）
        duration = get_video_duration(save_path)

        extract_first_frame_moviepy(save_path,thumbnail_path)
        # 9. 生成文件URL（根据你的实际部署环境调整）
        file_url = f"/api/video/{unique_filename}.{file_extension}"
        thumbnail_url= f"/api/thumbnail/{unique_filename}.jpg"




        id=system.video_manager.add_video(name,annotation,file_size,file_url,duration, thumbnail_url)
        if id==-1:
            os.remove(save_path)
            os.remove(thumbnail_path)


        response_data = {
            'code': 200,
            'message': '上传成功',
            'data': {
                'id': id,  # 生成简单ID，实际应该用数据库ID
                'name': name,
                'annotation': annotation,
                'size': file_size,
                'url': file_url,
                'duration': duration
            }
        }


        return success_response(data=response_data)

    except Exception as e:
        return error_response(str(e), 500)



@admin_bp.route('/feedback_all', methods=['GET'])
@jwt_required()
def feedback_all():
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
        if user['role'] != 'admin':
            return error_response('权限不足', 401)

        feedbacks = system.feedback_manager.get_all_feedbacks()
        print(feedbacks)
        success_response(
            data={
                'id': user['id'],
                'feedbacks': feedbacks
            }
        )
    except Exception as e:
        return error_response(str(e), 400)
