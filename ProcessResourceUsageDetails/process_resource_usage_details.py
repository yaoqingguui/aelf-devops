"""
    When the total amount of system resources reaches the threshold, an alarm is triggered,
    and information on the top processes consuming system resources is collected.
"""

import os
import subprocess
import sys


def available_mem():
    command = "cat /proc/meminfo | grep MemAvailable | awk '{print $2}'"
    available_mem_kb = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        encoding="utf-8")
    output, error = available_mem_kb.communicate()
    return int(output)


def id_cpu():
    command = "vmstat | grep -v r | awk '{print $15}'"
    id_cpu_percentage = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         encoding="utf-8")
    output, error = id_cpu_percentage.communicate()
    return int(output)


def cpu_top3():
    command = "ps aux | grep -v PID | sort -rn -k +4 | head -n3 | awk '{print $2,$3,$4}'"
    cpu_top3_str = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    encoding="utf-8")
    output, error = cpu_top3_str.communicate()
    output_list = []
    for line in output.split(os.linesep):
        if line.split():
            output_list.append(line.split())
    return output_list


def mem_top3():
    command = "ps aux | grep -v PID | sort -rn -k +3 | head -n3 | awk '{print $2,$3,$4}'"
    mem_top3_str = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    encoding="utf-8")
    output, error = mem_top3_str.communicate()
    output_list = []
    for line in output.split(os.linesep):
        if line.split():
            output_list.append(line.split())
    return output_list


def pid_name_rss(pid):
    command = "cat /proc/" + str(pid) + "/status | egrep 'Name|RSS' | awk '{print $2}'"
    pid_name_rss_str = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        encoding="utf-8")
    output, error = pid_name_rss_str.communicate()
    output_list = output.split()
    return output_list


def main(resource, threshold):
    if resource == 'mem':
        mem_threshold_kb = int(threshold) * 1024
        available_mem_kb = available_mem()
        if available_mem_kb <= mem_threshold_kb:
            mem_top3_list = mem_top3()
            res_list = []
            for line in mem_top3_list:
                pid = line[0]
                res_list.append({'PID': pid, 'CPU': line[1], 'MEM': line[2], 'INFO': pid_name_rss(pid)})
            return res_list
        else:
            return None
    elif resource == 'cpu':
        cpu_threshold_percentage = 100 - int(threshold)
        id_cpu_percentage = id_cpu()
        if id_cpu_percentage <= cpu_threshold_percentage:
            cpu_top3_list = cpu_top3()
            res_list = []
            for line in cpu_top3_list:
                pid = line[0]
                res_list.append({'PID': pid, 'CPU': line[1], 'MEM': line[2], 'INFO': pid_name_rss(pid)})
            return res_list
        else:
            return None


if __name__ == '__main__':
    data_info = main(sys.argv[1], sys.argv[2])
    if data_info is not None:
        print(f"{data_info[0]}\n{data_info[1]}\n{data_info[2]}")
    else:
        print("Normal")
