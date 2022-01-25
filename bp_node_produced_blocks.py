"""
    监控aelf BP节点出块是否正常
    https://explorer.aelf.io/api/vote/getAllTeamDesc?isActive=true
    https://explorer.aelf.io/new-socket/?EIO=3&transport=polling
    https://explorer.aelf.io/new-socket/?EIO=3&transport=polling&sid=xMoxC1zi4cxzRY_yABQd
    https://explorer.aelf.io/vote/election
"""

import requests
import json
from my_db import MyDB


class NodeProducedBlocks(MyDB):
    def __init__(self):
        super().__init__()
        self.bp_node_url = self.config()['bp_node_url']
        self.node_info = self.config()['bp_node']
        self.table_name = "bp_node_produced_blocks"

    def create_table(self):
        sql = f'create table {self.table_name}(public_key varchar(255) not null, num int)'
        self.execute_up(sql)

    def select(self, key):
        sql = f'select num from {self.table_name} where public_key = "{key}"'
        select_res_list = self.execute_select(sql)
        if select_res_list:
            return select_res_list[0][0]
        else:
            return None

    def insert(self, key, num):
        sql = f"insert into {self.table_name} values('{key}', {num})"
        self.execute_up(sql)

    def update(self, key, num):
        sql = f"update {self.table_name} set num = {num} where public_key = '{key}'"
        self.execute_up(sql)

    def node_produced_blocks(self):
        while True:
            params = {"EIO": 3, "transport": "polling"}
            data_sid_str = requests.get(url=self.bp_node_url, params=params).text  # 获取 sid
            params["sid"] = data_sid_str.split('"')[3]
            new_data_str = requests.get(url=self.bp_node_url, params=params).text  # 获取最终数据
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

    def main(self):
        bp_produced_blocks = self.node_produced_blocks()
        data_list = []
        for node in self.node_info:
            name = node['name']
            address = node['address']
            public_key = node['public_key']
            db_blocks = self.select(public_key)
            chain_blocks = bp_produced_blocks[public_key]
            if db_blocks is None:
                self.insert(public_key, chain_blocks)
                continue
            if chain_blocks > db_blocks:
                pass
            else:
                data_dict = {"name": name, "address": address, "public_key": public_key, "quantity": chain_blocks}
                data_list.append(data_dict)

            self.update(public_key, chain_blocks)
        return data_list


if __name__ == '__main__':
    node_data = NodeProducedBlocks()
    try:
        res_data = node_data.main()
        if res_data:
            print(res_data)
        else:
            print("BP_Produced_Blocks_Normal")
    except:
        node_data.create_table()  # 初始化数据库表
