#!/usr/bin/env bash
# 在主服务环境中，启动flower监控
celery -A celery_server flower --address=0.0.0.0 --port=5550
