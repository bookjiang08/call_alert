# -*- coding: utf-8 -*-

import sys
from aliyunsdkdyvmsapi.request.v20170525 import SingleCallByTtsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider

reload(sys)
sys.setdefaultencoding('utf8')

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dyvmsapi"
DOMAIN = "dyvmsapi.aliyuncs.com"

# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "*****"
ACCESS_KEY_SECRET = "*****"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME,REGION,DOMAIN)

def tts_call(called_number, tts_param=None, business_id=uuid.uuid1(), called_show_number="073182705509", tts_code='TTS_147435338'):
    ttsRequest = SingleCallByTtsRequest.SingleCallByTtsRequest()
    # 申请的语音通知tts模板编码,必填
    ttsRequest.set_TtsCode(tts_code)
    # 设置业务请求流水号，必填。后端服务基于此标识区分是否重复请求的判断
    ttsRequest.set_OutId(business_id)
    # 语音通知的被叫号码，必填。
    ttsRequest.set_CalledNumber(called_number)
    # 语音通知显示号码，必填。
    ttsRequest.set_CalledShowNumber(called_show_number)
    # tts模板变量参数
    if tts_param is not None:
        ttsRequest.set_TtsParam(tts_param)
    # 调用tts文本呼叫接口，返回json
    ttsResponse = acs_client.do_action_with_exception(ttsRequest)
    return ttsResponse

#if __name__ == '__main__':
#    params = {"taskname":"服务12345", "name":"陈禹"}
#    params = json.dumps(params)
#    print tts_call("152*********", params)
