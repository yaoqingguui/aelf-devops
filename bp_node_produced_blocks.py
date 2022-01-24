"""
    监控aelf BP节点出块是否正常
"""

import requests
import json
import sys


def node_produced_blocks(address):
    while True:
        params = {"EIO": 3, "transport": "polling"}
        data_sid_str = requests.get(url=url, params=params).text  # 获取 sid
        params["sid"] = data_sid_str.split('"')[3]
        new_data_str = requests.get(url=url, params=params).text  # 获取最终数据
        new_data_list = list(new_data_str)
        while True:
            if new_data_list[0] == '[':
                break
            else:
                del new_data_list[0]

        res_data_str = "".join(new_data_list)  # list 转 str

        try:
            res_data_dict = json.loads(res_data_str)[1]
            for k, v in res_data_dict.items():
                if k == address:
                    return v
            break
        # except Exception as e:
        #     print(e)
        except:
            continue


if __name__ == '__main__':
    url = "https://explorer.aelf.io/new-socket/"
    node_address = sys.argv[1]
    num = node_produced_blocks(node_address)
    print(num)
