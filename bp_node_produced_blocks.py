"""
    监控aelf BP节点出块是否正常
    https://explorer.aelf.io/api/vote/getAllTeamDesc?isActive=true
    https://explorer.aelf.io/new-socket/?EIO=3&transport=polling
    https://explorer.aelf.io/new-socket/?EIO=3&transport=polling&sid=xMoxC1zi4cxzRY_yABQd
"""

import requests
import json
import my_db

from config import LoadConf


def node_produced_blocks():
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
            return res_data_dict
        except:
            continue


def select(key):
    sql = f'select num from bp_node_produced_blocks where public_key = "{key}"'
    select_res_list = my_db.execute_select(sql)
    if select_res_list:
        return select_res_list[0][0]
    else:
        return None


def insert(key, num):
    sql = f"insert into bp_node_produced_blocks values('{key}', {num})"
    my_db.execute_up(sql)


def update(key, num):
    sql = f"update bp_node_produced_blocks set num = {num} where public_key = '{key}'"
    my_db.execute_up(sql)


if __name__ == '__main__':
    load_conf = LoadConf()
    conf = load_conf.conf_info()
    url = conf['bp_node_url']
    bp_produced_blocks = node_produced_blocks()
    # print(bp_produced_blocks)
    node_info = conf['bp_node']

    for node in node_info:
        name = node['name']
        address = node['address']
        public_key = node['public_key']
        db_blocks = select(public_key)
        chain_blocks = bp_produced_blocks[public_key]
        if db_blocks is None:
            insert(public_key, chain_blocks)
            continue
        if chain_blocks > db_blocks:
            print("BP_Produced_Blocks_Normal")
        else:
            information = f"name: {name}\naddress: {address}\npublic_key: {public_key}\nquantity: {chain_blocks}"
            print(information)

        update(public_key, chain_blocks)
