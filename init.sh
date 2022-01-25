#!/bin/bash

set -e

echo "Include=/etc/zabbix/zabbix_agentd.d/aelf-devops/*.conf" >> /etc/zabbix/zabbix_agentd.conf
chmod -R 777 sqlite3/
/etc/init.d/zabbix-agent restart
