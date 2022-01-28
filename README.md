# aelf-devops

## Install
```shell
bash <(curl -s "https://raw.githubusercontent.com/AElfProject/aelf-devops/main/init.sh") install
```
### verify
output node height
```shell
python3 /etc/zabbix/zabbix_agentd.d/aelf-devops/aelf_node_status_info.py block_height
```

Output node synchronization delay time, in seconds
```shell
python3 /etc/zabbix/zabbix_agentd.d/aelf-devops/aelf_node_status_info.py sync_status
```

Output BP_Produced_Blocks_Normal is normal
```shell
python3 /etc/zabbix/zabbix_agentd.d/aelf-devops/bp_node_produced_blocks.py
```


## Update
```shell
bash <(curl -s "https://raw.githubusercontent.com/AElfProject/aelf-devops/main/init.sh") update

```


## Uninstall
```shell
bash <(curl -s "https://raw.githubusercontent.com/AElfProject/aelf-devops/main/init.sh") uninstall

```