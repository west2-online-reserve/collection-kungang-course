# 宠物相册路由
from flask import Blueprint, request, jsonify
import datetime

photo_bp = Blueprint('photos', __name__)

# 这里简化处理，实际应该使用文件上传
# 可以集成 OSS 或本地文件存储

def get_db_connection():
    """获取数据库连接 - 需要从主应用导入"""
    from app import get_db_connection as get_conn
    return get_conn()

@photo_bp.route('/api/animals/<int:animal_id>/photos', methods=['GET'])
def get_animal_photos(animal_id):
    """获取动物的所有照片"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT p.*, u.username 
            FROM animal_photos p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.animal_id = %s
            ORDER BY p.created_at DESC
        """, (animal_id,))
        photos = cur.fetchall()
        return jsonify([dict(photo) for photo in photos]), 200
    finally:
        cur.close()
        conn.close()

@photo_bp.route('/api/animals/<int:animal_id>/photos', methods=['POST'])
def upload_animal_photo(animal_id):
    """上传动物照片"""
    from app import token_required
    
    @token_required
    def _upload(current_user):
        data = request.json
        photo_url = data.get('photo_url')
        description = data.get('description', '')
        
        if not photo_url:
            return jsonify({'message': '请提供照片URL'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO animal_photos (animal_id, user_id, photo_url, description, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING photo_id
            """, (animal_id, current_user['user_id'], photo_url, description, datetime.datetime.now()))
            photo_id = cur.fetchone()['photo_id']
            conn.commit()
            return jsonify({'message': '照片上传成功', 'photo_id': photo_id}), 201
        finally:
            cur.close()
            conn.close()
    
    return _upload()

@photo_bp.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """删除照片"""
    from app import token_required
    
    @token_required
    def _delete(current_user):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # 检查权限：只能删除自己上传的照片，或管理员可以删除任何照片
            cur.execute("SELECT user_id FROM animal_photos WHERE photo_id = %s", (photo_id,))
            photo = cur.fetchone()
            
            if not photo:
                return jsonify({'message': '照片不存在'}), 404
            
            if photo['user_id'] != current_user['user_id'] and current_user['role'] != '管理员':
                return jsonify({'message': '无权删除此照片'}), 403
            
            cur.execute("DELETE FROM animal_photos WHERE photo_id = %s", (photo_id,))
            conn.commit()
            return jsonify({'message': '照片删除成功'}), 200
        finally:
            cur.close()
            conn.close()
    
    return _delete()
