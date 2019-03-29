for i in `ps -ef | grep uwsgi | grep -v grep | grep -v tailf | awk '{print $2}'`; do kill -9 $i;done
rm -rf /opt/script/call_alert/alert_api/uwsgi.pid
/opt/script/alertvenv/bin/uwsgi /opt/script/call_alert/alert_api/uwconfig.ini
