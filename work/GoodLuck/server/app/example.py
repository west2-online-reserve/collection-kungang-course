import datetime
import hashlib
import os
from pathlib import Path

from . import config
from flask import Flask, request, jsonify, Blueprint, send_file,send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from jwt import ExpiredSignatureError, InvalidTokenError



from .api.tools import error_response, success_response, hash_password


example_bp = Blueprint('example', __name__, url_prefix='/api')
from .database import get_db

system=get_db(config.DataBase_Name)

@example_bp.route('/media/videos', methods=['GET'])
@jwt_required()
def get_media_videos():
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

    videos=system.video_manager.get_all_video_records()

    return success_response(data=videos)


@example_bp.route('/video/<filename>')

def video(filename):
    try:
        # print(f"请求视频文件: {filename}")

        # 获取项目根目录（app 文件夹的父目录）
        base_dir = Path(__file__).parent.parent  # 这会指向 app 的父目录
        video_path = base_dir / config.VIDEO_FOLDER / filename

        # print(f"视频完整路径: {video_path}")
        # print(f"路径是否存在: {video_path.exists()}")

        if not video_path.exists():
            return jsonify({"error": "视频文件不存在"}), 404

        # 使用 send_file 自动处理范围请求
        # print("使用 send_file 自动处理范围请求")
        response = send_file(
            str(video_path),  # 转换为字符串
            as_attachment=False,
            conditional=True,
            mimetype='video/mp4'
        )

        # 添加必要的响应头
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Cache-Control'] = 'no-cache'

        # print("文件发送成功")
        return response

    except Exception as e:
        print(f"服务器错误详情: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

@example_bp.route('/thumbnail/<filename>')

def thumbnail(filename):
    try:
        # print(f"请求视频文件: {filename}")

        # 获取项目根目录（app 文件夹的父目录）
        base_dir = Path(__file__).parent.parent  # 这会指向 app 的父目录
        thumbnail_path = base_dir / config.THUMBNAIL_FOLDER / filename
        print(f"查找文件路径: {thumbnail_path}")
        print(f"文件是否存在: {thumbnail_path.exists()}")
        if not thumbnail_path.exists():
            return jsonify({"error": "缩略图不存在"}), 404

        # 直接返回图片文件
        return send_file(str(thumbnail_path))

    except Exception as e:
        print(f"<UNK>: {str(e)}")
    # 返回错误图片
        return send_file('static/error.jpg', mimetype='image/jpeg')
