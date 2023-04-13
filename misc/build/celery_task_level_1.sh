#!/usr/bin/env bash
# 启动主任务

bash misc/build/celery.sh -q task_level_1 -c 3 -n task_level_1_worker -m 100 -l info
