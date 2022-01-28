#!/bin/bash

# cd /etc/zabbix/zabbix_agentd.d/ && git clone https://github.com/AElfProject/aelf-devops.git && cd aelf-devops/

# set -e
GITHUB_URL="https://github.com/AElfProject/aelf-devops.git"
#FOLDER_DIR=$(cd "$(dirname "$0")";pwd)
FOLDER_DIR="/etc/zabbix/zabbix_agentd.d/aelf-devops"
CONFIG_FILE="/etc/zabbix/zabbix_agentd.conf"

CONF_NUM=$(grep -Ev "^#|^$" ${CONFIG_FILE}| grep -c "Include=${FOLDER_DIR}")
PIP_PACKAGE=$(dpkg -l | grep -c "python3-pip")  # 检查 Ubuntu 系统是否安装 python3-pip 软件包

#[ ! -d ${FOLDER_DIR} ] && echo "${FOLDER_DIR} 目录不存在" && exit 1;

git clone ${GITHUB_URL} ${FOLDER_DIR}

[ "${PIP_PACKAGE}" -eq 0 ] && apt install -y python3-pip

pip3 install -r "${FOLDER_DIR}"/requestments.txt
[ $? -ne 0 ] && exit 0

[ "${CONF_NUM}" -eq 0 ] && echo "Include=${FOLDER_DIR}/zabbix-user-parameter.conf" >> ${CONFIG_FILE}

chmod -R 777 "${FOLDER_DIR}"/sqlite3/

/etc/init.d/zabbix-agent restart

