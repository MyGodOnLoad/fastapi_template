#!/usr/bin/env bash

export PROJECT_ENV=prod
nohup bash misc/build/celery_task_level_1.sh > logs/task_level_1_worker.log &

nohup bash misc/build/celery_task_level_2.sh > logs/task_level_2_worker.log &

nohup bash misc/build/flower.sh &

python main.py -e prod
