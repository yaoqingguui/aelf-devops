"""
    Monitor the block height and block time difference of AELF nodes
"""

import requests
import json
import time
import sys


def node_block_height(ip="127.0.0.1"):
    block_url = f"http://{ip}:8000/api/blockChain/blockHeight"
    height_num_str = requests.get(url=block_url).text
    return int(height_num_str)


def node_block_height_utctime(height_num, ip="127.0.0.1"):
    height_url = f"http://{ip}:8000/api/blockChain/blockByHeight"
    params = {"blockHeight": height_num}
    res_date_str = requests.get(url=height_url, params=params).text
    res_date_str = json.loads(res_date_str)  # Format data as dictionary format
    utc_time = res_date_str["Header"]["Time"]
    return utc_time


if __name__ == '__main__':
    # test_ip = "18.185.93.36"
    try:
        num = node_block_height()
        if sys.argv[1] == "block_height":
            print(num)
        elif sys.argv[1] == "sync_status":
            block_utc_time = node_block_height_utctime(num)
            local_time = time.localtime(time.time())
            local_time_stamp = int(time.mktime(local_time))
            block_utc_time_str = f"{block_utc_time.split('T')[0]} {block_utc_time.split('T')[1].split('.')[0]}"
            block_utc_time_array = time.strptime(block_utc_time_str, "%Y-%m-%d %H:%M:%S")
            block_utc_time_stamp = int(time.mktime(block_utc_time_array))
            time_diff = local_time_stamp - block_utc_time_stamp
            print(time_diff)
        else:
            pass

    except requests.exceptions.ConnectionError as e:
        print(e)
