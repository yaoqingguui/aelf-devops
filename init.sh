#!/bin/bash

# git clone https://github.com/AElfProject/aelf-devops.git

# set -e

CONFIG_FILE="/etc/zabbix/zabbix_agentd.conf"

FOLDER_DIR=$(cd "$(dirname "$0")";pwd)

CONF_NUM=$(grep -Ev "^#|^$" ${CONFIG_FILE}| grep -c "Include=${FOLDER_DIR}")

pip3 install -r "${FOLDER_DIR}"/requestments.txt

[ $? -ne 0 ] && exit 0

[ "${CONF_NUM}" -eq 0 ] && echo "Include=${FOLDER_DIR}/*.conf" >> ${CONFIG_FILE}

chmod -R 777 "${FOLDER_DIR}"/sqlite3/

/etc/init.d/zabbix-agent restart

