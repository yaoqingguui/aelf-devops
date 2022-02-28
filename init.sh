#!/bin/bash

set -e

GITHUB_URL="https://github.com/AElfProject/aelf-devops.git"
#FOLDER_DIR=$(cd "$(dirname "$0")";pwd)
FOLDER_DIR="/etc/zabbix/zabbix_agentd.d/aelf-devops"
CONFIG_FILE="/etc/zabbix/zabbix_agentd.conf"
CONF_NUM=$(grep -Ev "^#|^$" ${CONFIG_FILE}| grep -c "Include=${FOLDER_DIR}")


install_scripts() {
  git clone ${GITHUB_URL} ${FOLDER_DIR}
  PIP_PACKAGE=$(dpkg -l | grep -c "python3-pip")
  [ "${PIP_PACKAGE}" -eq 0 ] && apt install -y python3-pip
  pip3 install -r "${FOLDER_DIR}"/requestments.txt
  #[ $? -ne 0 ] && exit 0
  [ "${CONF_NUM}" -eq 0 ] && echo "Include=${FOLDER_DIR}/zabbix-user-parameter.conf" >> ${CONFIG_FILE}
  chmod -R 777 "${FOLDER_DIR}"/sqlite3/
}


uninstall_scripts() {
  [ "${CONF_NUM}" -ne 0 ] && sed -i '/aelf-devops/d' ${CONFIG_FILE}
  date=$(date "+%Y%m%d-%H%M")
  mv ${FOLDER_DIR} /tmp/aelf-devops-"${date}"
}


update_scripts() {
  if [ -d "${FOLDER_DIR}" ]; then
    cd ${FOLDER_DIR} && { git pull && [ $? -ne 0 ] && exit 0; }
    FILE_NUM=$(grep -Ev "^#|^$" ${CONFIG_FILE}| grep "zabbix-user-parameter.conf"|grep -c "Include=${FOLDER_DIR}")

    if [ "${CONF_NUM}" -ne 0 ] && [ "${FILE_NUM}" -eq 0 ]; then
      sed -i '/aelf-devops/d' ${CONFIG_FILE}
      echo "Include=${FOLDER_DIR}/zabbix-user-parameter.conf" >> ${CONFIG_FILE}
    fi;
    pip3 install -r "${FOLDER_DIR}"/requestments.txt
  else
    install_scripts
  fi
}


restart_server() {
  /etc/init.d/zabbix-agent restart
}


case "$1" in
    install)
        update_scripts
        restart_server
        ;;
    uninstall)
        uninstall_scripts
        restart_server
        ;;
#    update)
#        update_scripts
#        restart_server
#        ;;
    *)
        echo "Usage: $0 {install|uninstall|update}"
        exit 2
esac

