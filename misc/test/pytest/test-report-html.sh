#!/usr/bin/env bash

set -e
set -x

pytest --cov=app --cov-report=html:test_report/cov_report --html=test_report/result_report.html misc/test/pytest --capture=sys --self-contained-html "${@}"