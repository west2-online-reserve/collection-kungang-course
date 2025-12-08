from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import jwt
import datetime
from functools import wraps
import hashlib

# 导入配置文件
try:
    from config import DB_CONFIG, SECRET_KEY
except ImportError:
    print("警告: 未找到 config.py 文件，使用默认配置")
    DB_CONFIG = {
        'host': 'localhost',
        'port': 8000,
        'database': 'stray_animal_db',
        'user': 'your_username',
        'password': 'your_password'
    }
    SECRET_KEY = 'your-secret-key-change-in-production'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': '缺少认证令牌'}), 401
        try:
            token = token.split(' ')[1] if ' ' in token else token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data
        except:
            return jsonify({'message': '认证令牌无效'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.get('role') != '管理员':
            return jsonify({'message': '需要管理员权限'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# User Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        password_hash = hash_password(data['password'])
        cur.execute(
            "INSERT INTO users (username, password_hash, role, contact) VALUES (%s, %s, %s, %s) RETURNING user_id",
            (data['username'], password_hash, data.get('role', '普通用户'), data.get('contact', ''))
        )
        user_id = cur.fetchone()['user_id']
        conn.commit()
        return jsonify({'message': '注册成功', 'user_id': user_id}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({'message': '用户名已存在'}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = hash_password(data['password'])
    cur.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", 
                (data['username'], password_hash))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user:
        token = jwt.encode({
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token, 'user': dict(user)}), 200
    return jsonify({'message': '用户名或密码错误'}), 401

# Animal Archive Routes
@app.route('/api/animals', methods=['GET'])
def get_animals():
    conn = get_db_connection()
    cur = conn.cursor()
    
    zone = request.args.get('zone')
    status = request.args.get('status')
    is_sterilized = request.args.get('is_sterilized')
    
    query = "SELECT * FROM animals WHERE 1=1"
    params = []
    
    if zone:
        query += " AND zone = %s"
        params.append(zone)
    if status:
        query += " AND status = %s"
        params.append(status)
    if is_sterilized is not None:
        query += " AND is_sterilized = %s"
        params.append(is_sterilized == 'true')
    
    cur.execute(query, params)
    animals = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(animal) for animal in animals]), 200

@app.route('/api/animals/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM animals WHERE animal_id = %s", (animal_id,))
    animal = cur.fetchone()
    cur.close()
    conn.close()
    if animal:
        return jsonify(dict(animal)), 200
    return jsonify({'message': '动物不存在'}), 404

@app.route('/api/animals', methods=['POST'])
@token_required
def create_animal(current_user):
    if current_user['role'] != '管理员':
        return jsonify({'message': '权限不足，需要管理员权限'}), 403
    
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 检查是否已存在同名动物
        cur.execute("SELECT animal_id FROM animals WHERE name = %s", (data['name'],))
        existing = cur.fetchone()
        if existing:
            return jsonify({'message': f'已存在名为"{data["name"]}"的动物，请使用不同的名字'}), 400
        
        cur.execute(
            """INSERT INTO animals (name, species, zone, status, is_sterilized, photo_url, found_date) 
               VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING animal_id""",
            (data['name'], data['species'], data['zone'], 
             data.get('status', '流浪中'), data.get('is_sterilized', False), 
             data.get('photo_url', ''), data.get('found_date', datetime.date.today()))
        )
        animal_id = cur.fetchone()['animal_id']
        conn.commit()
        return jsonify({'message': '动物档案创建成功', 'animal_id': animal_id}), 201
    finally:
        cur.close()
        conn.close()

@app.route('/api/animals/<int:animal_id>', methods=['PUT'])
@token_required
def update_animal(current_user, animal_id):
    if current_user['role'] != '管理员':
        return jsonify({'message': '权限不足，需要管理员权限'}), 403
    
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """UPDATE animals SET name=%s, species=%s, zone=%s, status=%s, 
               is_sterilized=%s, photo_url=%s, found_date=%s WHERE animal_id=%s""",
            (data['name'], data['species'], data['zone'], data['status'],
             data['is_sterilized'], data.get('photo_url', ''), 
             data.get('found_date'), animal_id)
        )
        conn.commit()
        return jsonify({'message': '动物信息更新成功'}), 200
    finally:
        cur.close()
        conn.close()

@app.route('/api/animals/<int:animal_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_animal(current_user, animal_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM animals WHERE animal_id = %s", (animal_id,))
        conn.commit()
        return jsonify({'message': '动物档案删除成功'}), 200
    finally:
        cur.close()
        conn.close()

# Feed Records Routes
@app.route('/api/feed-records', methods=['GET'])
@token_required
def get_feed_records(current_user):
    conn = get_db_connection()
    cur = conn.cursor()
    
    animal_id = request.args.get('animal_id')
    query = """SELECT fr.*, u.username, a.name as animal_name 
               FROM feed_records fr 
               JOIN users u ON fr.user_id = u.user_id 
               JOIN animals a ON fr.animal_id = a.animal_id"""
    params = []
    
    if animal_id:
        query += " WHERE fr.animal_id = %s"
        params.append(animal_id)
    
    query += " ORDER BY fr.feed_time DESC"
    cur.execute(query, params)
    records = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(record) for record in records]), 200

@app.route('/api/feed-records', methods=['POST'])
@token_required
def create_feed_record(current_user):
    # 所有登录用户都可以添加投喂记录
    
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO feed_records (user_id, animal_id, feed_time, food_content) 
               VALUES (%s, %s, %s, %s) RETURNING record_id""",
            (current_user['user_id'], data['animal_id'], 
             data.get('feed_time', datetime.datetime.now()), data['food_content'])
        )
        record_id = cur.fetchone()['record_id']
        conn.commit()
        return jsonify({'message': '投喂记录创建成功', 'record_id': record_id}), 201
    finally:
        cur.close()
        conn.close()

# Health Logs Routes
@app.route('/api/health-logs', methods=['GET'])
@token_required
def get_health_logs(current_user):
    conn = get_db_connection()
    cur = conn.cursor()
    
    animal_id = request.args.get('animal_id')
    query = """SELECT hl.*, a.name as animal_name 
               FROM health_logs hl 
               JOIN animals a ON hl.animal_id = a.animal_id"""
    params = []
    
    if animal_id:
        query += " WHERE hl.animal_id = %s"
        params.append(animal_id)
    
    query += " ORDER BY hl.log_date DESC"
    cur.execute(query, params)
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(log) for log in logs]), 200

@app.route('/api/health-logs', methods=['POST'])
@token_required
def create_health_log(current_user):
    if current_user['role'] != '管理员':
        return jsonify({'message': '权限不足，需要管理员权限'}), 403
    
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO health_logs (animal_id, action_type, cost, log_date, description) 
               VALUES (%s, %s, %s, %s, %s) RETURNING log_id""",
            (data['animal_id'], data['action_type'], data['cost'], 
             data.get('log_date', datetime.date.today()), data.get('description', ''))
        )
        log_id = cur.fetchone()['log_id']
        conn.commit()
        return jsonify({'message': '医疗记录创建成功', 'log_id': log_id}), 201
    finally:
        cur.close()
        conn.close()

# Adoption Application Routes
@app.route('/api/adoptions', methods=['GET'])
@token_required
def get_adoptions(current_user):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if current_user['role'] == '管理员':
        query = """SELECT aa.*, u.username, a.name as animal_name 
                   FROM adoption_applications aa 
                   JOIN users u ON aa.user_id = u.user_id 
                   JOIN animals a ON aa.animal_id = a.animal_id 
                   ORDER BY aa.create_time DESC"""
        cur.execute(query)
    else:
        query = """SELECT aa.*, a.name as animal_name 
                   FROM adoption_applications aa 
                   JOIN animals a ON aa.animal_id = a.animal_id 
                   WHERE aa.user_id = %s 
                   ORDER BY aa.create_time DESC"""
        cur.execute(query, (current_user['user_id'],))
    
    applications = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(app) for app in applications]), 200

@app.route('/api/adoptions', methods=['POST'])
@token_required
def create_adoption(current_user):
    data = request.json
    
    # 验证必填字段
    if not data.get('animal_id'):
        return jsonify({'message': '请选择要领养的动物'}), 400
    if not data.get('apply_reason') or not data.get('apply_reason').strip():
        return jsonify({'message': '请填写申请理由'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Check if animal is available
        cur.execute("SELECT status FROM animals WHERE animal_id = %s", (data['animal_id'],))
        animal = cur.fetchone()
        if not animal:
            return jsonify({'message': '动物不存在'}), 404
        if animal['status'] == '已领养':
            return jsonify({'message': '该动物已被领养'}), 400
        if animal['status'] == '已死亡':
            return jsonify({'message': '该动物已死亡'}), 400
        
        # 检查是否已经申请过
        cur.execute(
            """SELECT COUNT(*) as count FROM adoption_applications 
               WHERE user_id = %s AND animal_id = %s AND status = '待审核'""",
            (current_user['user_id'], data['animal_id'])
        )
        existing = cur.fetchone()
        if existing and existing['count'] > 0:
            return jsonify({'message': '您已经提交过该动物的领养申请，请等待审核'}), 400
        
        cur.execute(
            """INSERT INTO adoption_applications (user_id, animal_id, status, apply_reason, create_time) 
               VALUES (%s, %s, %s, %s, %s) RETURNING application_id""",
            (current_user['user_id'], data['animal_id'], '待审核', 
             data['apply_reason'].strip(), datetime.datetime.now())
        )
        app_id = cur.fetchone()['application_id']
        conn.commit()
        return jsonify({'message': '领养申请已提交', 'application_id': app_id}), 201
    except Exception as e:
        conn.rollback()
        print(f"创建领养申请失败: {e}")
        return jsonify({'message': f'提交失败: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/adoptions/<int:app_id>/approve', methods=['PUT'])
@token_required
@admin_required
def approve_adoption(current_user, app_id):
    data = request.json
    new_status = data['status']  # '已通过' or '已驳回'
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Get application details
        cur.execute("SELECT animal_id FROM adoption_applications WHERE application_id = %s", (app_id,))
        app = cur.fetchone()
        if not app:
            return jsonify({'message': '申请不存在'}), 404
        
        # Update application status
        cur.execute("UPDATE adoption_applications SET status = %s WHERE application_id = %s", 
                   (new_status, app_id))
        
        # If approved, update animal status
        if new_status == '已通过':
            cur.execute("UPDATE animals SET status = '已领养' WHERE animal_id = %s", 
                       (app['animal_id'],))
        
        conn.commit()
        status_text = '通过' if new_status == '已通过' else '驳回'
        return jsonify({'message': f'申请已{status_text}'}), 200
    finally:
        cur.close()
        conn.close()

# Statistics Routes
@app.route('/api/statistics/sterilization', methods=['GET'])
def get_sterilization_stats():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT is_sterilized, COUNT(*) as count 
        FROM animals 
        GROUP BY is_sterilized
    """)
    stats = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(stat) for stat in stats]), 200

@app.route('/api/statistics/zone-distribution', methods=['GET'])
def get_zone_distribution():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT zone, COUNT(*) as count 
        FROM animals 
        GROUP BY zone 
        ORDER BY count DESC
    """)
    stats = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(stat) for stat in stats]), 200

@app.route('/api/statistics/monthly-costs', methods=['GET'])
def get_monthly_costs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            TO_CHAR(log_date, 'YYYY-MM') as month,
            SUM(cost) as total_cost
        FROM health_logs
        WHERE log_date >= CURRENT_DATE - INTERVAL '6 months'
        GROUP BY TO_CHAR(log_date, 'YYYY-MM')
        ORDER BY month
    """)
    stats = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(stat) for stat in stats]), 200

@app.route('/api/statistics/animal-costs', methods=['GET'])
def get_animal_costs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.animal_id, a.name, COALESCE(SUM(hl.cost), 0) as total_cost
        FROM animals a
        LEFT JOIN health_logs hl ON a.animal_id = hl.animal_id
        GROUP BY a.animal_id, a.name
        ORDER BY total_cost DESC
    """)
    stats = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(stat) for stat in stats]), 200

# User Management Routes (Admin only)
@app.route('/api/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, role, contact, created_at FROM users ORDER BY user_id")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@token_required
@admin_required
def update_user_role(current_user, user_id):
    data = request.json
    new_role = data.get('role')
    
    if new_role not in ['管理员', '普通用户']:
        return jsonify({'message': '无效的角色'}), 400
    
    # 不能修改自己的角色
    if user_id == current_user['user_id']:
        return jsonify({'message': '不能修改自己的角色'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET role = %s WHERE user_id = %s", (new_role, user_id))
        conn.commit()
        return jsonify({'message': '角色更新成功'}), 200
    finally:
        cur.close()
        conn.close()

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, user_id):
    # 不能删除自己
    if user_id == current_user['user_id']:
        return jsonify({'message': '不能删除自己的账号'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        return jsonify({'message': '用户删除成功'}), 200
    finally:
        cur.close()
        conn.close()

# Animal Photos Routes
@app.route('/api/animals/<int:animal_id>/photos', methods=['GET'])
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

@app.route('/api/animals/<int:animal_id>/photos', methods=['POST'])
@token_required
def upload_animal_photo(current_user, animal_id):
    """上传动物照片"""
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

@app.route('/api/photos/<int:photo_id>', methods=['DELETE'])
@token_required
def delete_photo(current_user, photo_id):
    """删除照片"""
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
