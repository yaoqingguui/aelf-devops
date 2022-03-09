from os import environ, path
import paramiko
import math
import re
import tempfile
import os

INPUT_HOST_PORT = environ.get("INPUT_HOST_PORT")
INPUT_PORT = int(environ.get("INPUT_PORT", "22"))
INPUT_USER = environ.get("INPUT_USER")
INPUT_PASS = environ.get("INPUT_PASS")
INPUT_SSH_PRIVATE_KEY = environ.get("INPUT_KEY")
INPUT_CONNECT_TIMEOUT = environ.get("INPUT_CONNECT_TIMEOUT", "30s")
INPUT_SCRIPT = environ.get("INPUT_SCRIPT")

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "M": 86400 * 30}
pattern_seconds_per_unit = re.compile(r'^(' + "|".join(['\\d+' + k for k in seconds_per_unit.keys()]) + ')$')


def convert_to_seconds(s):
    if s is None:
        return 30
    if isinstance(s, str):
        return int(s[:-1]) * seconds_per_unit[s[-1]] if pattern_seconds_per_unit.search(s) else 30
    if (isinstance(s, int) or isinstance(s, float)) and not math.isnan(s):
        return round(s)
    return 30


def ssh_process():
    if INPUT_SCRIPT is None or INPUT_SCRIPT == "" or (INPUT_SSH_PRIVATE_KEY is None and INPUT_PASS is None):
        print("SSH invalid (Script/Key/Passwd)")
        return

    print("+++++++++++++++++++Pipeline: RUNNING SSH+++++++++++++++++++")
    hp = [c.strip() for c in INPUT_HOST_PORT.splitlines() if c is not None]
    print(hp)

    commands = [c.strip() for c in INPUT_SCRIPT.splitlines() if c is not None]
    print(f"commands: {commands}")
    command_str = ""

    for i in range(len(commands)):
        c = path.expandvars(commands[i])
        if c == "":
            continue
        if c.endswith('&&') or c.endswith('||') or c.endswith(';'):
            c = c[0:-2] if i == (len(commands) - 1) else c
        else:
            c = f"{c} &&" if i < (len(commands) - 1) else c
        command_str = f"{command_str} {c}"
    command_str = command_str.strip()
    print(command_str)

    with paramiko.SSHClient() as ssh:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        try:
            p_key = None
            if INPUT_SSH_PRIVATE_KEY:
                tmp.write(INPUT_SSH_PRIVATE_KEY.encode())
                tmp.close()
                p_key = paramiko.RSAKey.from_private_key_file(filename=tmp.name)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"p_key: {p_key}")
            for line in hp:
                host_port = line.split(':')
                if len(host_port) > 1:
                    host = host_port[0]
                    port = host_port[1]
                else:
                    host = host_port[0]
                    port = INPUT_PORT

                ssh.connect(host, port=port, username=INPUT_USER, pkey=p_key, password=INPUT_PASS,
                            timeout=convert_to_seconds(INPUT_CONNECT_TIMEOUT))

                stdin, stdout, stderr = ssh.exec_command(command_str)
                out = "".join(stdout.readlines())
                out = out.strip() if out is not None else None
                if out:
                    print(f"Success: \n{out}")

                err = "".join(stderr.readlines())
                err = err.strip() if err is not None else None
                if err:
                    if out is None:
                        raise Exception(err)
                    else:
                        print(f"Error: \n{err}")
        finally:
            os.unlink(tmp.name)
            tmp.close()


if __name__ == '__main__':
    ssh_process()
