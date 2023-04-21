#!/usr/bin/env bash
# 启动子任务

celery -A celery_server worker -n task_level_2@%h -l info -Q task_level_2 --max-tasks-per-child 100
