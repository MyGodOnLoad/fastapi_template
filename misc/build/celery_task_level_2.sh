#!/usr/bin/env bash
# 启动子任务

bash misc/build/celery.sh -q task_level_2 -c 3 -n task_level_2_worker -m 100 -l info
