# AELF-DEVOPS

## Install or Update
```shell
$ bash <(curl -s "https://raw.githubusercontent.com/AElfProject/aelf-devops/main/init.sh") install
```

## Uninstall
```shell
$ bash <(curl -s "https://raw.githubusercontent.com/AElfProject/aelf-devops/main/init.sh") uninstall
```

## verify

- Node height

  ```shell
  $ python3 /etc/zabbix/aelf-devops/aelf_node_status_info.py block_height
  ```

- Node synchronization delay time, in seconds

  ```shell
  $ python3 /etc/zabbix/aelf-devops/aelf_node_status_info.py sync_status
  ```

- BP_Produced_Blocks_Normal is normal

  ```shell
  $ python3 /etc/zabbix/aelf-devops/bp_node_produced_blocks.py
  ```

- When the system resource usage reaches the threshold, output the top 3 processes that occupy the most resources

  ```shell
  $ python3 /etc/zabbix/aelf-devops/ProcessResourceUsageDetails/process_resource_usage_details.py cpu 95
  
  $ python3 /etc/zabbix/aelf-devops/ProcessResourceUsageDetails/process_resource_usage_details.py mem 300
  ```

  