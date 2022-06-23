#!/bin/bash

#set -e

ServerIP="${2:-172.31.15.92}"

GITHUB_URL="https://github.com/AElfProject/aelf-devops.git"
#FOLDER_DIR=$(cd "$(dirname "$0")";pwd)
OLD_FOLDER_DIR="/etc/zabbix/zabbix_agentd.d/aelf-devops"
FOLDER_DIR="/etc/zabbix/aelf-devops"


Ubuntu_Version_ID=$(grep "VERSION_ID" /etc/os-release | awk -F '"' '{print $2}')
if [ "${Ubuntu_Version_ID}" = "16.04" ]; then
  CONFIG_FILE="/etc/zabbix/zabbix_agentd.conf"
  agent_client_server="/etc/init.d/zabbix-agent"
  agent_name="zabbix-agent"
elif [ "${Ubuntu_Version_ID}" = "18.04" ] || [ "${Ubuntu_Version_ID}" = "20.04" ]; then
  CONFIG_FILE="/etc/zabbix/zabbix_agent2.conf"
  agent_client_server="/etc/init.d/zabbix-agent2"
  agent_name="zabbix-agent2"
else
  echo "System version mismatch"
  exit 1
fi


remove_agent() {
  agent_num=$(dpkg -l |grep  "^ii"|awk '{print $2}' |grep -wc zabbix-agent)
  if [ "${agent_num}" -ne 0 ]; then
    systemctl stop zabbix-agent.service
    cp -a /etc/zabbix /etc/zabbox_bak_"$(date '+%Y%m%d-%H%M%S')"
    dpkg -l |grep  "^ii"|awk '{print $2}' |grep -E zabbix | xargs apt-get --purge remove -y
  fi
}


config_agent2() {
  sed -i "s#Server=127.0.0.1#Server=${ServerIP}#g" "${CONFIG_FILE}"
  sed -i "s#ServerActive=127.0.0.1#ServerActive=${ServerIP}#g" "${CONFIG_FILE}"

  if [ -d "${OLD_FOLDER_DIR}" ]; then
    cp -a ${OLD_FOLDER_DIR} ${FOLDER_DIR}
  fi
}


install_agent2() {
  agent2_num=$(dpkg -l |grep  "^ii"|awk '{print $2}' |grep -wc zabbix-agent2)
  if [ "${agent2_num}" -eq 0 ]; then
#    Ubuntu_Version_ID=$(grep "VERSION_ID" /etc/os-release | awk -F '"' '{print $2}')
    if [ ! -f "/tmp/zabbix-release_6.0-1+ubuntu${Ubuntu_Version_ID}_all.deb" ]; then
      wget --no-check-certificate \
      https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.0-1+ubuntu"${Ubuntu_Version_ID}"_all.deb \
      -P /tmp
    fi
    dpkg -i /tmp/zabbix-release_6.0-1+ubuntu"${Ubuntu_Version_ID}"_all.deb
    apt -y update
    apt install -y ${agent_name}
    config_agent2
  fi
}


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
  CONF_NUM=$(grep -Ev "^#|^$" ${CONFIG_FILE}| grep -c "Include=${FOLDER_DIR}")
  [ "${CONF_NUM}" -ne 0 ] && sed -i '/aelf-devops/d' ${CONFIG_FILE}
  date=$(date "+%Y%m%d-%H%M")
  mv ${FOLDER_DIR} /tmp/aelf-devops-"${date}"
}


update_scripts() {
  CONF_NUM=$(grep -Ev "^#|^$" ${CONFIG_FILE}| grep -c "Include=${FOLDER_DIR}")

  if [ -d "${FOLDER_DIR}" ]; then
    cd ${FOLDER_DIR} && { git pull && [ $? -ne 0 ] && exit 0; }
    FILE_NUM=$(grep -Ev "^#|^$" ${CONFIG_FILE}| grep "zabbix-user-parameter.conf"|grep -c "Include=${FOLDER_DIR}")

    if [ "${CONF_NUM}" -ne 0 ] && [ "${FILE_NUM}" -eq 0 ]; then
      sed -i '/aelf-devops/d' ${CONFIG_FILE}
      echo "Include=${FOLDER_DIR}/zabbix-user-parameter.conf" >> ${CONFIG_FILE}
    elif [ "${CONF_NUM}" -eq 0 ] && [ "${FILE_NUM}" -eq 0 ]; then
      echo "Include=${FOLDER_DIR}/zabbix-user-parameter.conf" >> ${CONFIG_FILE}
    else
      echo "1"
    fi;
    pip3 install -r "${FOLDER_DIR}"/requestments.txt

  else
    install_scripts
  fi
}


restart_server() {
  ${agent_client_server} restart
}


case "$1" in
  install)
    remove_agent && sleep 1
    install_agent2 && sleep 1

    update_scripts
    restart_server
    ;;
  uninstall)
    uninstall_scripts
    restart_server
    ;;
  *)
    echo "Usage: $0 {install|uninstall}"
    exit 2
esac
