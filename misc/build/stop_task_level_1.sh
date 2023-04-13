#!/usr/bin/env bash

# grep your tag~
ps aux | grep -i task_level_1 | awk '{print $2}' | xargs kill -9
