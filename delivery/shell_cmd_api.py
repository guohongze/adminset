# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE

def cmd_exec(cmd):
    out_str = []
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data_out = p.stdout.read()
    data_err = p.stderr.read()
    if data_out != "":
        out_str.append(data_out)
    if data_err != "":
        out_str.append(data_err)
    return ",".join(out_str)