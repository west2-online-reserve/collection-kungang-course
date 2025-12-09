import datetime
import hashlib
import json
import os
import threading
import time
import uuid
from .api import process_side
from .api import process_front
import requests
from flask import Flask, request, jsonify, Blueprint, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.utils import secure_filename
from .api.celery_tasks import process_video_task
from . import config
from .redis_manager import redis_manager


from .api.tools import error_response, success_response, hash_password


upload_bp = Blueprint('upload', __name__, url_prefix='/api')
from .database import get_db

system=get_db(config.DataBase_Name)

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
# conversation={}
# tasks = {}
#
# user_task={}
# def process_video(task_id,front_video_path, side_video_path):
#     try:
#         side=process_side.process(side_video_path)
#         front,num=process_front.process(front_video_path)
#         if side is None or front is None:
#             raise Exception('视频处理失败，请检查视频清晰度或背景颜色')
#         result = {
#             'message': front+side,
#         }
#         # 更新任务状态
#         tasks[task_id]['status'] = 'completed'
#         tasks[task_id]['result'] = result
#         tasks[task_id]['project']='引体向上'+str(num)+'个'
#
#
#     except Exception as e:
#         tasks[task_id]['status'] = 'error'
#         tasks[task_id]['message'] = str(e)


@upload_bp.route('/clear',methods=['GET'])
@jwt_required()
def clear():
    print('clear')
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
    # if user_task.get(user_id):
    #
    #     tasks[user_task[user_id]]=None
    #     user_task[user_id] = None
    # if conversation.get(user_id):
    #
    #     conversation[user_id]=''
    redis_manager.delete_task(redis_manager.get_user_task(user_id))
    redis_manager.clear_conversation(user_id)


    return success_response()



@upload_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload():
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

    if 'front_video' not in request.files or 'side_video' not in request.files:
        return jsonify({'success': False, 'message': '请上传正面和侧面两个视频'})

    front_video = request.files['front_video']
    side_video = request.files['side_video']

    # 检查文件是否选择
    if front_video.filename == '' or side_video.filename == '':
        return jsonify({'success': False, 'message': '请选择视频文件'})

    # 检查文件格式
    if not (allowed_file(front_video.filename) and allowed_file(side_video.filename)):
        return jsonify({'success': False, 'message': '不支持的文件格式'})

    # 生成任务ID
    task_id = str(uuid.uuid4())


    # 保存文件
    front_filename = secure_filename(front_video.filename)
    side_filename = secure_filename(side_video.filename)

    front_path = os.path.join(config.UPLOAD_FOLDER, f"{task_id}_front_{front_filename}")
    side_path = os.path.join(config.UPLOAD_FOLDER, f"{task_id}_side_{side_filename}")

    front_video.save(front_path)
    side_video.save(side_path)


    redis_manager.create_task(task_id,{
        'status': 'processing',
        'result': None
    })

    # 初始化任务状态
    # tasks[task_id] = {
    #     'status': 'processing',
    #     'result': None
    # }

    # 在后台处理视频评估
    # thread = threading.Thread(
    #     target=process_video,
    #     args=(task_id, front_path, side_path)
    # )
    # thread.daemon = True
    # thread.start()
    async_task = process_video_task.delay(task_id, front_path, side_path, user_id)

    # 存储Celery任务ID
    redis_manager.update_task(task_id, {
        'celery_task_id':async_task.id,
        'user_id': user_id,
    })

    redis_manager.set_user_task(user_id, task_id)
    # tasks[task_id]['celery_task_id'] = async_task.id
    # tasks[task_id]['user_id'] = user_id
    # print('taskid',task_id)
    # print('celery_id',tasks[task_id]['celery_task_id'])


    print(redis_manager.get_task(task_id))



    return jsonify({
        'success': True,
        'task_id': task_id,
        'message': '视频上传成功，正在分析中...'
    })


@upload_bp.route('/evaluate/result/<task_id>', methods=['GET'])
@jwt_required()
def get_evaluation_result(task_id):
    """
    获取评估结果
    """
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


    # if task_id not in tasks:
    #     return jsonify({'success': False, 'message': '任务不存在'})
    # if  task_id!=user_task[user_id]:
    #     return jsonify({'success': False, 'message': '权限不足'})

    # task = tasks[task_id]
    #
    # if task['status'] == 'completed':
    #     print(task['result'])
    #     return jsonify({
    #         'success': True,
    #         'status': 'completed',
    #         'result': task['result']
    #     })
    # elif task['status'] == 'processing':
    #     return jsonify({
    #         'success': True,
    #         'status': 'processing',
    #         'message': '视频分析中...'
    #     })
    # else:
    #     return jsonify({
    #         'success': False,
    #         'status': 'error',
    #         'message': '分析过程中出现错误'
    #     })
    # 检查任务是否存在
    # if task_id not in tasks:
    #     return jsonify({'success': False, 'message': '任务不存在'})
    #
    #     # 检查任务权限
    # if tasks[task_id]['user_id'] != user_id:
    #     return jsonify({'success': False, 'message': '权限不足'})

    if redis_manager.get_task(task_id) is None:
        return jsonify({'success': False, 'message': '任务不存在'})

    # print(redis_manager.get_task(task_id),user_id)
    if redis_manager.get_task(task_id)['user_id'] != int(user_id):
        return jsonify({'success': False, 'message': '权限不足'})

    # task = tasks[task_id]
    task=redis_manager.get_task(task_id)
    # print(task)


    # 如果有Celery任务ID，查询任务状态
    if 'celery_task_id' in task:
        celery_task = process_video_task.AsyncResult(task['celery_task_id'])

        if celery_task.ready():
            if celery_task.successful():
                result = celery_task.result
                task['status'] = 'completed'
                task['result'] = result.get('result')
                task['project'] = result.get('project')
                redis_manager.update_task(task_id, task)
            else:
                task['status'] = 'error'
                task['error'] = str(celery_task.result)

    if task['status'] == 'completed':
        return jsonify({
            'success': True,
            'status': 'completed',
            'result': task['result'],
            'project': task.get('project', '')
        })
    elif task['status'] == 'processing':
        return jsonify({
            'success': True,
            'status': 'processing',
            'message': '视频分析中...'
        })
    elif task['status'] == 'error':
        return jsonify({
            'success': False,
            'status': 'error',
            'message': task.get('error', '分析过程中出现错误')
        })
    else:
        return jsonify({
            'success': False,
            'status': 'unknown',
            'message': '未知的任务状态'
        })


@upload_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat_stream():
    """处理聊天请求并返回流式响应"""
    data = request.json
    user_input = data.get('message')
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

    conversation_id=redis_manager.get_conversation(user_id)
    # conversation_id=conversation.get(user_id,'')
    print(conversation_id)

    def generate():
        # 调用 Dify API
        url = config.DIFY_API_URL
        headers = {
            "Authorization": f"Bearer {config.DIFY_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": {},
            "query": user_input,
            "response_mode": "streaming",
            "user": user_id,
            "conversation_id": conversation_id
        }

        # print(conversation.get(user_id,''))
        # print(payload)


        response = requests.post(url, json=payload, headers=headers, stream=True)
        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True):
                # print(line)
                if line and line.startswith('data:'):


                    data = line[5:]  # 移除 'data:' 前缀
                    try:

                        data_dict = json.loads(data)
                        # if conversation.get(user_id, '') == '':
                        #     conversation[user_id] = data_dict.get('conversation_id', '')
                        if redis_manager.get_conversation(user_id) == '':
                            redis_manager.set_conversation(user_id, data_dict.get('conversation_id',''))


                        if data_dict['event'] == 'message_end':
                            # yield f"data: {json.dumps({'event': 'end'})}\n\n"
                            break

                        # 提取关键信息
                        event_data = {
                            'content': data_dict.get('answer', ''),

                        }

                        yield f"data: {json.dumps(event_data)}\n\n"

                    except json.JSONDecodeError:
                        continue
        else:
            error_data = {'error': f'请求失败: {response.status_code}'}
            yield f"data: {json.dumps(error_data)}\n\n"

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    )

@upload_bp.route('/save', methods=['POST'])
@jwt_required()
def save():
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

        msg=request.json['message'].replace('*','').replace('#','').replace('-','')


        line=msg.split('\n')
        message=''
        score=None
        for line in line:
            line = line.strip()
            if line.startswith('评分'):
                try :

                    score=int(line[3:].strip())
                except ValueError:
                    continue
            elif line !='':
                message=message+line+'\n'

        # print(score)
        # print(message)
        project=redis_manager.get_task(redis_manager.get_user_task(user_id))['project']


        rid=system.rating_manager.add_rating(score,message)
        system.history_manager.add_history_record(user['id'],rid,project)
        return success_response('保存记录成功')
    except Exception as e:
        return error_response('服务错误', 500)

