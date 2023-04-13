import unittest
from BeautifulReport import BeautifulReport

from core.lib import cfg


BASE_PATH = cfg.get_root_path()

# 单元测试报告
discovery = unittest.defaultTestLoader.discover(BASE_PATH)
runner = BeautifulReport(discovery)
runner.report(filename='report', description='单元测试报告',
              report_dir='test_report', theme='theme_default')
