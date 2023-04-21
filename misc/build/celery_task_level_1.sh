#!/usr/bin/env bash
# 启动主任务

celery -A celery_server worker -n task_level_1@%h -l info -Q task_level_1 --max-tasks-per-child 100
