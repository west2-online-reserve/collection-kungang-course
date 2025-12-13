# app/celery_app.py
from celery import Celery
import os
from . import config


def make_celery(app_name=__name__):
    # 从配置文件读取Redis配置，如果没有则使用默认值
    redis_host = getattr(config, 'REDIS_HOST', 'localhost')
    redis_port = getattr(config, 'REDIS_PORT', 6379)
    redis_url = f"redis://{redis_host}:{redis_port}/0"

    # 注意：include路径要正确指向任务模块
    celery = Celery(
        app_name,
        broker=redis_url,
        backend=redis_url,
        include=['app.api.celery_tasks']  # 修改为绝对路径
    )

    # 配置
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Shanghai',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=300,  # 5分钟超时
        task_soft_time_limit=240,  # 4分钟软超时
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=100,
        broker_connection_retry_on_startup=True,
        # 添加更多配置
        task_acks_late=True,  # 任务完成后才确认
        task_reject_on_worker_lost=True,  # worker丢失时重新排队
    )

    return celery


# 创建全局Celery实例
celery_app = make_celery()