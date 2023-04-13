#!/usr/bin/env bash

# grep your tag~
ps aux | grep -i main.py | awk '{print $2}' | xargs kill -9
