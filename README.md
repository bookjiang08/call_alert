### call_alert项目说明
#### 一. 依赖环境
- 语言：Python2.7
- 组件：nginx，uwsgi，阿里云sdk

#### 二. 部署说明（默认路径：/opt/script/call_alert/）
##### 1. 安装相关组件
- 创建虚拟环境

```
virtualenv alertvenv
source alertvenv/bin/activate
```

- 安装通用依赖库

```
pip install -r requirements.txt
```

- 安装阿里云sdk库

```
wget -c http://ytx-sdk.oss-cn-shanghai.aliyuncs.com/dyvms_python.zip 
unzip dyvms_python.zip
cd ./dyvms_python/api_sdk/aliyun-python-sdk-core
python setup.py install

cd ./dyvms_python/api_sdk/aliyun-python-sdk-dyvmsapi
python setup.py install
```

- 安装nignx

```
yum install -y nginx

```

##### 2. 组件配置
- uwsgi配置

```
[uwsgi]
chdir=/opt/script/call_alert/alert_api 

home=/opt/script/alertvenv

socket = 127.0.0.1:5678

wsgi-file = /opt/script/call_alert/alert_api/manager.py

callable = app

processes = 1

threads = 2

pidfile = /var/lib/uwsgi.pid

daemonize = /opt/script/call_alert/logs/uwsgi.log

lazy-apps = true              # 使用worker进程重载

touch-chain-reload = true     # 修改文件自动重载

listen = 10                   # 设置socket监听队列大小

buffer-size = 32768           # 设置请求头的大小

vacuum=true                   # 当服务器退出时自动删除unix socket文件和pid文件

```

- nginx配置

```
events {
        worker_connections  1024;
}
http {
     include       mime.types;
     default_type  application/octet-stream;
     sendfile        on;
     keepalive_timeout  65;
     server {
            listen 8765;
            server_name your_ip;
            access_log  /opt/script/call_alert/logs/ng_access.log;
            error_log /opt/script/call_alert/logs/ng_error.log;
            charset utf-8;
            client_max_body_size 5M;
            location / {
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:5678;
            }
     }
}
```

#### 三. 启动说明
- 启动uwsgi

```
cd /opt/script/call_alert/alert_api
uwsgi --ini uwconfig.ini
```

- 启动nginx

```
systemctl start nginx
```

#### 四. 接口说明：
- 请求方式：POST
- 请求URL：http://your_ip:8765/phoneWarn/callUp/v1/gen
- 接口输入参数说明

参数名 | 类型|说明
---- | --- | --- 
tos | String | 手机号码(必填)
name |  String |告警姓名(必填)
content| String |告警信息(必填，需处理ip地址，否则报关键字黑名单)

- 接口输出说明

参数名|类型|说明
---|---|---
Message| String | 请求结果信息
Code| String |返回码

- 输出信息

```
# 请求成功：
"result": {
    "CallId": "115400978362^102205443362",
    "Message": "OK",
    "Code": "OK",
    "RequestId": "9F6D1B0A-A370-4B23-B77A-9D4C54C67188"
}

# 请求失败：
"result": {
    "Code": "isv.BLACK_KEY_CONTROL_LIMIT",
    "Message": "模板变量中存在黑名单关键字",
    "RequestId": "409EC708-C0BF-49D9-BCA1-3A0D1F0AE921"
}
```


