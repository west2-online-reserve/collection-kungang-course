# app/redis_manager.py (新增部分)
import json
import redis
from datetime import timedelta
from . import config


class RedisManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=0,
            decode_responses=True  # 注意：存储JSON时需特殊处理
        )

    # ============== 任务字典管理 (核心新增部分) ==============
    def create_task(self, task_id, initial_data=None):
        """
        创建新任务记录
        initial_data: 初始数据，如 {'status': 'processing', 'user_id': 123}
        """
        key = f"task:{task_id}"
        data = initial_data or {}
        data.setdefault('created_at', self._current_time())
        data.setdefault('status', 'pending')

        # 使用哈希表存储，方便更新单个字段
        mapping = {k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
                   for k, v in data.items()}

        # 设置24小时过期
        pipeline = self.redis_client.pipeline()
        pipeline.hset(key, mapping=mapping)
        pipeline.expire(key, timedelta(hours=24))
        pipeline.execute()

        return True

    def update_task(self, task_id, updates):
        """
        更新任务信息（部分字段）
        updates: 要更新的字段字典，如 {'status': 'processing', 'progress': 50}
        """
        key = f"task:{task_id}"
        if not self.redis_client.exists(key):
            return False

        # 准备更新的字段
        update_data = {}
        for field, value in updates.items():
            if isinstance(value, (dict, list)):
                update_data[field] = json.dumps(value, ensure_ascii=False)
            else:
                update_data[field] = str(value)

        if update_data:
            self.redis_client.hset(key, mapping=update_data)

        return True

    def get_task(self, task_id):
        """
        获取完整任务信息
        """
        key = f"task:{task_id}"
        data = self.redis_client.hgetall(key)

        if not data:
            return None

        # 反序列化JSON字段
        result = {}
        for field, value in data.items():
            # 尝试解析JSON
            if value.startswith('{') or value.startswith('['):
                try:
                    result[field] = json.loads(value)
                except json.JSONDecodeError:
                    result[field] = value
            elif value.lower() in ('true', 'false'):
                result[field] = value.lower() == 'true'
            elif value.isdigit():
                result[field] = int(value)
            else:
                result[field] = value

        return result

    def delete_task(self, task_id):
        """删除任务记录"""
        key = f"task:{task_id}"
        return self.redis_client.delete(key)

    def task_exists(self, task_id):
        """检查任务是否存在"""
        key = f"task:{task_id}"
        return self.redis_client.exists(key) > 0

    def set_task_result(self, task_id, result, project=None):
        """
        专门设置任务结果（完成时调用）
        """
        updates = {
            'status': 'completed',
            'result': result,
            'completed_at': self._current_time()
        }
        if project:
            updates['project'] = project

        return self.update_task(task_id, updates)

    def set_task_error(self, task_id, error_message):
        """
        设置任务错误状态
        """
        return self.update_task(task_id, {
            'status': 'error',
            'error': error_message,
            'failed_at': self._current_time()
        })

    # ============== 辅助方法 ==============
    def _current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().isoformat()

    # ============== 之前的用户任务和对话管理方法保持不变 ==============
    def set_user_task(self, user_id, task_id, expire_hours=24):
        """关联用户和其最新的任务ID"""
        key = f"user_task:{user_id}"
        self.redis_client.setex(key, timedelta(hours=expire_hours), task_id)
        return True

    def get_user_task(self, user_id):
        """获取用户最新的任务ID"""
        key = f"user_task:{user_id}"
        return self.redis_client.get(key)

    # ... 其他已有方法保持不变 ...
    def set_conversation(self, user_id, conversation_id, expire_hours=24):
        """设置用户的对话ID"""
        key = f"conversation:{user_id}"
        self.redis_client.setex(key, timedelta(hours=expire_hours), conversation_id)
        return True

    def get_conversation(self, user_id):
        """获取用户的对话ID"""
        key = f"conversation:{user_id}"
        result=self.redis_client.get(key)
        return result if result is not None else ''

    def clear_conversation(self, user_id):
        """清除用户的对话ID"""
        key = f"conversation:{user_id}"
        return self.redis_client.delete(key)


# 创建全局实例
redis_manager = RedisManager()