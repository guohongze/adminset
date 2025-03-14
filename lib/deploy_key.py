
from subprocess import Popen, PIPE


def deploy_key(ip, ssh_pwd):
    cmd = "/usr/bin/expect /var/opt/adminset/main/lib/sshkey_deploy {} {}".format(ip, ssh_pwd)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    # 在Python 3中，子进程的输出是字节流，需要解码为字符串
    stdout = stdout.decode('utf-8', errors='replace') if stdout else ''
    stderr = stderr.decode('utf-8', errors='replace') if stderr else ''
    return stdout, stderr
