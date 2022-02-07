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
        error_log_list = []
        for logs in self.swap_oracle_client_log:
            if os.path.exists(logs):
                # command = f"grep -r '\[ERR\]' {logs} | grep '{old_1_min}'"
                command = f"grep -r '\[ERR\]' {logs} | grep -E '2022-02-05 01:5|2021-09-08 17:43|2021-09-13 12:22|2021-09-12 04:5'"
                error_log = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                             encoding="utf-8")
                output, error = error_log.communicate()
                if len(output.split(os.linesep)) > 1:
                    error_log_list = error_log_list + output.split(os.linesep)
        return error_log_list


if __name__ == '__main__':
    swap_oracle_client = SwapOracleClientError()
    error_list = swap_oracle_client.check_error_log()

    new_error_list = []
    for line in error_list:
        if line:
            new_error_list.append(line)

    if new_error_list:
        error_str = '\n'.join(new_error_list)
    else:
        error_str = "Log_Normal"
    print(error_str)
    # for line in error_list:
    #     print(line)

    # ll = ["", "", ""]
    # ll_new = []
    # for line in ll:
    #     if line:
    #         ll_new.append(line)
    #
    # print(ll_new)
    # ss = '\n'.join(ll_new)
    # print(ss)
    # if ss:
    #     print('111')

