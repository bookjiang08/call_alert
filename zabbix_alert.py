#!/opt/script/alertvenv/bin/python
# -*- coding: utf-8 -*-
# update: 20190128

import os
import sys
import json
import logging
import requests
from datetime import datetime
from interval import IntervalSet
from tools import tool

#time_range = '21:00--10:30'
#result = {"status":1,"data":"呼叫成功","message":null,"errorCode":null,"exceptionMsg":null,"success":true}


path = os.path.dirname(os.path.abspath(__file__))
log_name ='{}/{}-alert.log'.format(os.path.join(path, 'logs'), datetime.now().strftime("%Y-%m-%d"))
logging.basicConfig(level=logging.INFO,
                    filename=log_name,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger('alert')

call_user = {
    "1": {"phone": "1860********", "name": "xxxxxx"}
}

def call_on(call_user, subject):
    convert_subject = tool.ip_convert(subject)
    call_subject = convert_subject.split(':')[2].strip().replace('.','点')
    url = 'http://apiserver:8765/phoneWarn/callUp/v1/gen'
    payload = {'tos': call_user['1']["phone"], 'name': call_user['1']["name"], 'content': call_subject}
    result = requests.post(url, data=payload)
    alert_data = {"alert_data": subject.split(':')[2].strip(), "alert_name": call_user[num]['name']}
    log_info = {}
    log_info["info"] = alert_data
    log_info["result"] = json.loads(result.text.strip())
    logger.info(json.dumps(log_info))

if __name__ == '__main__':
    subject = sys.argv[1]
    start_time = IntervalSet.between("21:00", "23:59")
    end_time = IntervalSet.between("00:00", "10:30")
    now_time = datetime.now().strftime('%H:%M')
    alert_time = datetime.now().strftime("%Y%m%d")
    if now_time in start_time or now_time in end_time:
        call_on(call_user, subject)
    else:
        logger.info('非电话报警时间，报警取消..')
