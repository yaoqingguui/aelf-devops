import requests
import json


if __name__ == '__main__':
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    url = 'https://web-wallet.aelf.io/chain/api/blockChain/chainStatus'
    res_data_str = requests.get(url=url, headers=headers).text
    data_json = json.loads(res_data_str)
    print(data_json["BestChainHeight"])

