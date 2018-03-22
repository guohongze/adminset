# -*- coding: utf-8 -*-
import socket

def host_network_probe(ip,port):
    """IP 格式支持单个IP 或 IP地址列表，或 <IP,IP>格式"""
    def network_test(access,ip_port):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)
        try:
            sk.connect((str(I), int(port)))
            sk.close()
            return ["True",access,str(ip_port)]
        except Exception:
            sk.close()
            return ["False",access,str(ip_port)]
    if isinstance(ip, list):
        new_ip = ip
    else:
        new_ip = ",".split(ip)
    network_test_out = []
    for I in new_ip:
        test_out = network_test(I, port)
        network_test_out.append(",".join(test_out))
    return ",".join(network_test_out)
