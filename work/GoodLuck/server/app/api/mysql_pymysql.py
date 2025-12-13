import pymysql
import datetime
from typing import List, Dict, Optional
from pymysql.cursors import DictCursor
from .tools import hash_password

class DatabaseConfig:
    """数据库配置类"""
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database


class DatabaseConnection:
    """数据库连接管理"""
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None

    def get_connection(self):
        """获取数据库连接"""
        if not self.connection or self.connection.open == False:
            self.connection = pymysql.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                cursorclass=DictCursor,
                autocommit=False
            )
        return self.connection

    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()


class DatabaseInspector:
    """数据库信息查看工具"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def show_table_info(self):
        """显示所有表信息（简化版）"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT TABLE_NAME, TABLE_ROWS, CREATE_TIME 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = %s
            """, (self.db_connection.config.database,))
            return cursor.fetchall()


# ==================== 数据访问层（Manager类） ====================
class UserManager:
    """用户管理"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def add_user(self, username, password, height=None, weight=None ,role='user'):
        """添加用户"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO users (username, password, height, weight,role)
                    VALUES (%s, %s, %s, %s ,%s)
                """
                cursor.execute(sql, (username, password, height, weight,role))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"添加用户失败: {e}")
            return False

    def get_user_by_username(self, username):
        """通过用户名查询用户"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()

    def get_all_users(self):
        """获取所有用户"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, height, weight ,role FROM users")
            return cursor.fetchall()

    def update_user(self, userid,username, password=None, height=None, weight=None, role=None):
        """更新用户信息"""
        conn = self.db_connection.get_connection()
        try:
            updates = []
            params = []
            if username:
                updates.append("username = %s")
                params.append(username)
            if password:
                updates.append("password = %s")
                params.append(password)
            if height is not None:
                updates.append("height = %s")
                params.append(height)
            if weight is not None:
                updates.append("weight = %s")
                params.append(weight)
            if role is not None:
                updates.append("role = %s")
                params.append(role)
            if not updates:
                return False

            params.append(userid)

            # print(f"UPDATE users SET {', '.join(updates)} WHERE id = %s")
            # print(params)
            with conn.cursor() as cursor:
                sql = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
                cursor.execute(sql, params)
            conn.commit()

            return True
        except Exception as e:
            conn.rollback()
            print(f"更新用户失败: {e}")
            return False


class LoginManager:
    """登录记录管理"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def add_login_record(self, user_id):
        """添加登录记录"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO login_records (user_id, login_time) VALUES (%s, NOW())"
                cursor.execute(sql, (user_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"添加登录记录失败: {e}")
            return False

    def get_login_records_by_user(self, user_id):
        """获取用户登录记录"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, login_time FROM login_records 
                WHERE user_id = %s ORDER BY login_time DESC
            """, (user_id,))
            return cursor.fetchall()

    def get_all_login_records(self):
        """获取所有登录记录"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT lr.id, u.username, lr.login_time
                FROM login_records lr
                JOIN users u ON lr.user_id = u.id
                ORDER BY lr.login_time DESC
            """)
            return cursor.fetchall()


class RatingManager:
    """评分管理"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def add_rating(self, score,content):
        """添加评分"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO ratings (score,content) VALUES (%s,%s)"
                cursor.execute(sql, (score,content))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"添加评分失败: {e}")
            return -1

    def get_all_ratings(self):
        """获取所有评分"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, content FROM ratings")
            return cursor.fetchall()

    def get_rating_by_id(self, rating_id):
        """通过ID获取评分"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, content FROM ratings WHERE id = %s", (rating_id,))
            return cursor.fetchone()


class HistoryManager:
    """历史记录管理"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def add_history_record(self, user_id, rating_id,project):
        """添加历史记录"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO history_records (user_id, rating_id,project)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (user_id, rating_id,project))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"添加历史记录失败: {e}")
            return False

    def get_history_by_user(self, user_id):
        """获取用户历史记录"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT hr.id as id, hr.project as project,r.content as content, r.created_at as time,r.score as score
                FROM history_records hr
                JOIN ratings r ON hr.rating_id = r.id
                WHERE hr.user_id = %s
                ORDER BY r.created_at DESC
            """, (user_id,))
            return cursor.fetchall()

    def get_history_records_by_id(self, id):
        """<UNK>ID<UNK>"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT hr.id as id, hr.project as project,r.content as content, r.created_at as time,r.score as score
                FROM history_records hr
                JOIN ratings r ON hr.rating_id = r.id
                WHERE hr.id = %s
                ORDER BY r.created_at DESC
                    """,args=(id))
            return cursor.fetchall()

    def get_all_history_records(self):
        """获取所有历史记录"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT hr.id, u.username,hr.project, r.content, hr.record_time
                FROM history_records hr
                JOIN users u ON hr.user_id = u.id
                JOIN ratings r ON hr.rating_id = r.id
                ORDER BY hr.record_time DESC
            """)
            return cursor.fetchall()
class ExampleVideo:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
    def add_video(self, name,annotation,size,url,duration,thumbnail):
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO video_records (name,annotation,size,url,duration,thumbnail)
                    values (%s,%s,%s,%s,%s,%s)
                        """
                cursor.execute(sql, (name,annotation,size,url,duration,thumbnail))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"上传视频失败: {e}")
            conn.rollback()
            return -1

    def get_all_video_records(self):
        """<UNK>"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT id,name as title,annotation,size,url,duration,thumbnail
            FROM video_records
                """)
            return cursor.fetchall()


class TrainingPlanManager:
    """训练计划管理（新增功能）"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def add_training_plan(self, user_id, date,project,target,note):
        """添加训练计划"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO training_plans (user_id, date,project,target,note)
                    VALUES (%s, %s, %s,%s,%s)
                """
                cursor.execute(sql, (user_id, date,project, target,note))
            conn.commit()
            return cursor.lastrowid  # 返回新增计划ID
        except Exception as e:
            conn.rollback()
            print(f"添加训练计划失败: {e}")
            return -1

    def get_user_plans(self, user_id):
        """获取用户的所有训练计划"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id,  date,project,target,note,completed,actualCount
                FROM training_plans
                WHERE user_id = %s
                ORDER BY date DESC
            """, (user_id,))
            return cursor.fetchall()

    def get_plan_by_id(self, plan_id):
        """获取特定训练计划（验证归属）"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id,  date,project,target,note,completed,actualCount
                FROM training_plans
                WHERE id = %s 
            """, (plan_id))
            return cursor.fetchone()

    def update_training_plan(self, plan_id,user_id, target=None,note=None,completed=None,actualCount=None):
        """更新训练计划"""
        conn = self.db_connection.get_connection()
        try:
            updates = []
            params = []
            if target is not None:
                updates.append("target = %s")
                params.append(target)
            if note is not None:
                updates.append("note = %s")
                params.append(note)
            if completed is not None:
                updates.append("completed = %s")
                params.append(completed)
            if actualCount is not None:
                updates.append("actualCount = %s")
                params.append(actualCount)
            if not updates:
                return False  # 无更新内容

            params.extend([plan_id,user_id])
            with conn.cursor() as cursor:
                sql = f"""
                    UPDATE training_plans
                    SET {', '.join(updates)}
                    WHERE id = %s and user_id = %s
                """
                cursor.execute(sql, params)
            conn.commit()

            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"更新训练计划失败: {e}")
            return False

    def delete_training_plan(self, plan_id,user_id):
        """删除训练计划"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    DELETE FROM training_plans
                    WHERE id = %s and user_id = %s
                """
                cursor.execute(sql, (plan_id,user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"删除训练计划失败: {e}")
            return False

    def get_trained_date(self, user_id,year=None,month=None):
        keys=[]
        param=[]

        if year is not None:
            keys.append("and year(date)=%s ")
            param.append(year)
        if month is not None:
            keys.append("and month(date)=%s ")
            param.append(month)

        param.append(user_id)

        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            sql=f"""
               SELECT date
               FROM training_plans 
               WHERE user_id = %s {''.join(keys)}
               ORDER BY date DESC
               """

            print(sql)
            cursor.execute(sql, param)
            return cursor.fetchall()
class FeedbackManager:
    """用户反馈管理"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def add_feedback(self, user_id, content,email):  # 新增方法
        """添加用户反馈"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                      INSERT INTO  feedback (user_id, content ,email)
                      VALUES (%s,%s,%s) \
                      """
                cursor.execute(sql, (user_id, content,email))
            conn.commit()



            return cursor.lastrowid  # 返回新增计划ID
        except Exception as e:
            conn.rollback()
            print(f"添加反馈失败: {e}")
            return -1

    def get_feedback_by_id(self, id):  # 新增方法
        """获取用户的反馈"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT id, user_id, content, email,created_at
                           FROM feedback
                           WHERE id = %s
                           ORDER BY created_at DESC
                           """, (id,))
            return cursor.fetchall()

    def get_all_feedback(self):  # 新增方法
        """获取所有用户反馈"""
        conn = self.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id,user_id, content,email,created_at FROM feedback")
            return cursor.fetchall()

class ClassManagementSystem:
    """班级管理系统主类"""
    def __init__(self, config: DatabaseConfig):
        self.db_connection = DatabaseConnection(config)
        self.user_manager = UserManager(self.db_connection)
        self.login_manager = LoginManager(self.db_connection)
        self.rating_manager = RatingManager(self.db_connection)
        self.history_manager = HistoryManager(self.db_connection)
        self.training_plan_manager = TrainingPlanManager(self.db_connection)  # 新增
        self.feedback_manager = FeedbackManager(self.db_connection)
        self.video_manager=ExampleVideo(self.db_connection)

    def initialize(self):
        """初始化数据库表结构"""
        conn = self.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                # 用户表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(64) NOT NULL,  # 存储哈希后的密码
                        height DECIMAL(5,2) NULL,
                        weight DECIMAL(5,2) NULL,
                        role VARCHAR(10) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)


                # 登录记录表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS login_records (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        login_time DATETIME NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)

                # 评分表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ratings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        score DECIMAL(5,2) NOT NULL, 
                        content TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)

                # 历史记录表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history_records (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        rating_id INT NOT NULL,
                        project varchar(50) NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (rating_id) REFERENCES ratings(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)

                # 训练计划表（新增）
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS training_plans (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        date DATETIME NOT NULL,  # 训练计划时间
                        project varchar(50) NOT NULL,
                        target INT NOT NULL,  # 训练个数
                        note TEXT ,
                        completed bool NOT NULL default FALSE NOT NULL,
                        actualCount INT NOT NULL DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)

                #feedback
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        content TEXT NOT NULL,
                        email TEXT ,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                    """)

                #video_records (name,annotation,size,url,duration,thumbnail)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS video_records (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        annotation TEXT,
                        size int NOT NULL,
                        url TEXT NOT NULL,
                        duration DECIMAL(5,2) NOT NULL,
                        thumbnail TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                        """)


            conn.commit()

            self.user_manager.add_user('admin',hash_password('123456'),height=180,weight=70,role='admin')
            return True
        

        except Exception as e:
            conn.rollback()
            print(f"数据库初始化失败: {e}")
            return False



# 使用示例
