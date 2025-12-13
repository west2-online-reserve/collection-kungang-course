# app/api/celery_tasks.py
from app.celery_app import celery_app
import os
import json
from app.api import process_side, process_front
from app import config
from app.database import get_db

# 获取系统实例
system = get_db(config.DataBase_Name)


@celery_app.task(bind=True, name='process_video_task')
def process_video_task(self, task_id, front_video_path, side_video_path, user_id):
    """
    Celery任务：处理视频分析
    """
    try:

        # 更新任务进度
        self.update_state(
            state='PROCESSING',
            meta={
                'status': 'processing',
                'progress': 10,
                'message': '开始处理侧面视频...'
            }
        )

        # 处理侧面视频
        side = process_side.process(side_video_path)

        # 更新进度
        self.update_state(
            state='PROCESSING',
            meta={
                'status': 'processing',
                'progress': 50,
                'message': '侧面视频处理完成，开始处理正面视频...'
            }
        )

        # 处理正面视频
        front, num = process_front.process(front_video_path)

        if side is None or front is None:
            raise Exception('视频处理失败，请检查视频清晰度或背景颜色')

        # 构建结果
        result = {
            'message': front + side,
        }

        # 更新完成进度
        self.update_state(
            state='PROCESSING',
            meta={
                'status': 'processing',
                'progress': 90,
                'message': '视频处理完成，正在生成报告...'
            }
        )

        # 这里可以添加保存结果到数据库的逻辑
        # save_result_to_db(user_id, task_id, result, f'引体向上{num}个')

        return {
            'status': 'completed',
            'result': result,
            'project': f'引体向上{num}个',
            'progress': 100
        }

    except Exception as e:
        # 记录错误
        self.update_state(
            state='FAILURE',
            meta={
                'status': 'error',
                'progress': 0,
                'error': str(e)
            }
        )
        raise e