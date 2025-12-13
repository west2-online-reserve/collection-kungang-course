# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
max_requests = 1000
max_requests_jitter = 100
preload_app = True
# gunicorn.conf.py
# gunicorn.conf.py
import sys

# 将访问日志和错误日志都输出到stdout
accesslog = "-"
errorlog = "-"

# 捕获所有输出
capture_output = True
