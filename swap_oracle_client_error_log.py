
import datetime
import os

from config import LoadConf


old_1_min = (datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")


class SwapOracleClientError(LoadConf):
    def __init__(self):
        super().__init__()
        self.swap_oracle_client_log = self.config()['swap_oracle_client_log']

    def check_error_log(self):
        for logs in self.swap_oracle_client_log:
            if os.path.exists(logs):
                print(logs)


# grep -r "\[ERR\]" /opt/swap-oracle-client*/Logs/ | grep "2022-02-05 01:5"
if __name__ == '__main__':
    print(old_1_min)
    swap_oracle_client = SwapOracleClientError()
    print(swap_oracle_client.check_error_log())

