#!/usr/bin/env bash

ps aux | grep -i flower | awk '{print $2}' | xargs kill -9
