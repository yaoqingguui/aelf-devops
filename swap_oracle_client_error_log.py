import datetime
import os
import subprocess

from config import LoadConf


class SwapOracleClientError(LoadConf):
    def __init__(self):
        super().__init__()
        self.swap_oracle_client_log = self.config()['swap_oracle_client_log']

    def check_error_log(self):
        old_1_min = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
        for logs in self.swap_oracle_client_log:
            if os.path.exists(logs):
                # print(logs)
                command = f"grep -r '\[ERR\]' {logs} | grep '{old_1_min}'"
                error_log = subprocess.getoutput(command)
                # error_log = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                #                              encoding="utf-8")
                print(error_log)


# grep -r "\[ERR\]" /opt/swap-oracle-client*/Logs/ | grep "2022-02-05 01:5"
if __name__ == '__main__':
    swap_oracle_client = SwapOracleClientError()
    swap_oracle_client.check_error_log()
