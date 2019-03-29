# -*- coding: utf-8 -*-

import sys
sys.path.append('/opt/script/call_alert')

import os
import re
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from tools import call_method, tool

path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(path)
log_name ='{}/server.log'.format(os.path.join(parent_path, 'logs'))
logging.basicConfig(level=logging.INFO,
                    filename=log_name,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')

logger = logging.getLogger('server')

def create_app():
    app = Flask(__name__)
    api_prefix = '/phoneWarn/callUp/v1/'

    @app.route(api_prefix+'gen', methods=['POST'])
    def general_alert():
        content_name = request.form.get('name')
        phonenum = request.form.get('tos')
        call_content = request.form.get('content')
        params = {"taskname":"{}".format(call_content), "name":"{}".format(content_name),
                   "phonenum": "{}".format(phonenum)}
        logger.info(json.dumps(params, ensure_ascii=False))
        params.pop('phonenum', None)
        result = call_method.tts_call(phonenum, json.dumps(params))
        return jsonify(json.loads(result))

    @app.route(api_prefix+'db', methods=['POST'])
    def db_alert():
        content_name = '天元'
        alert_status = re.findall(r"\[(.*?)\]", request.form.get('content'))[1]
        alert_level = re.findall(r"\[(.*?)\]", request.form.get('content'))[0]
        if alert_status == 'PROBLEM' and alert_level < "P3":
            phonenum = request.form.get('tos')
            content_ip = re.findall(r"\[(.*?)\]", request.form.get('content'))[2]
            content_info = request.form.get('content').split(' ')[2]
            content_ip_convert = tool.ip_convert(content_ip)
            call_content = (content_ip_convert + content_info).replace('.', '点')
            params = {"taskname":"{}".format(call_content), "name":"{}".format(content_name),
                   "phonenum": "{}".format(phonenum)}
            params.pop('phonenum', None)
            result = call_method.tts_call(phonenum, json.dumps(params))
            print(json.loads(result))
        elif alert_status != 'PROBLEM':
            params = {"result": "恢复不报警.."}
        elif alert_level >= "P3":
            params = {"result": "报警等级大于P3，不报警"}
        else:
            params = {"result": "其他问题.."}
        logger.info(json.dumps(params, ensure_ascii=False))
        return json.dumps(params, ensure_ascii=False)

    return app
