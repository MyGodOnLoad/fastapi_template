import os
import time
from datetime import datetime
from time import localtime

from core.lib import logger
from core.lib.cfg import get_root_path


LOGGER = logger.for_service('scheduler')


def remove_temp_file():
    LOGGER.info('remove_temp_file 定时任务开始执行')
    root_path = get_root_path()
    temp_path = os.path.join(root_path, 'app', 'static', 'temp')

    file_list = os.listdir(temp_path)

    temp_file_list = []
    for file in file_list:
        if os.path.splitext(file)[-1] in ['.csv', '.json']:
            temp_file_list.append(file)

    today = datetime.today().date().strftime("%Y-%m-%d")
    for file in temp_file_list:
        file = os.path.join(temp_path, file)
        file_ctime = os.stat(file).st_mtime

        file_cdate = time.strftime("%Y-%m-%d", localtime(file_ctime))
        if file_cdate != today:
            # 删除
            os.remove(file)
            LOGGER.info(f"删除时间：{datetime.today()}  删除文件：{file}")
