# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import

import os, re, platform, socket, time, json, threading
import sys

# Python 2 和 3 兼容性导入
try:
    import psutil
    import schedule
    import requests
except ImportError:
    print("Please install required packages: psutil, schedule, requests")
    sys.exit(1)

from subprocess import Popen, PIPE
import logging

# Python 2.6+ 兼容性
try:
    json.loads
except AttributeError:
    import simplejson as json

# Python 2/3 兼容函数
def to_unicode(data):
    if sys.version_info[0] >= 3:
        # Python 3
        if isinstance(data, bytes):
            return data.decode('utf-8', errors='replace')
        return str(data)
    else:
        # Python 2
        if isinstance(data, str):
            return data.decode('utf-8', errors='replace')
        return unicode(data)

AGENT_VERSION = "1.0"
token = 'HPcWR7l4NJNJ'
# 更新服务器IP地址为日志显示的实际地址
server_ip = '192.168.110.100'
# 是否使用HTTPS
use_https = True
# 是否验证SSL证书
verify_ssl = False


def log(log_name, path=None):
    # 为了Python 3兼容性，使用文本模式而不是二进制模式
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y%m%d %H:%M:%S',
                filename=path+log_name,
                filemode='a+')  # 修改为'a+'模式
    return logging.basicConfig

log("agent.log", "/var/opt/adminset/client/")


def get_ip():
    try:
        hostname = socket.getfqdn(socket.gethostname())
        ipaddr = socket.gethostbyname(hostname)
    except Exception as msg:
        print(msg)
        ipaddr = ''
    return ipaddr


def get_dmi():
    p = Popen('dmidecode', stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return to_unicode(stdout) if stdout else ""


def parser_dmi(dmidata):
    pd = {}
    line_in = False
    for line in dmidata.split('\n'):
        if line.startswith('System Information'):
             line_in = True
             continue
        if line.startswith('\t') and line_in:
                 k,v = [i.strip() for i in line.split(':')]
                 pd[k] = v
        else:
            line_in = False
    return pd


def get_mem_total():
    cmd = "grep MemTotal /proc/meminfo"
    p = Popen(cmd, stdout=PIPE, shell = True)
    data = p.communicate()[0]
    # 解码二进制数据
    data_str = to_unicode(data)
    mem_total = data_str.split()[1]
    memtotal = int(round(int(mem_total)/1024.0/1024.0, 0))
    return memtotal


def get_cpu_model():
    cmd = "cat /proc/cpuinfo"
    p = Popen(cmd, stdout=PIPE, stderr = PIPE, shell = True)
    stdout, stderr = p.communicate()
    return stdout


def get_cpu_cores():
    cpu_cores = {"physical": psutil.cpu_count(logical=False) if psutil.cpu_count(logical=False) else 0, "logical": psutil.cpu_count()}
    return cpu_cores


def parser_cpu(stdout):
    if not stdout:
        return {}
    stdout = to_unicode(stdout)
    groups = [i for i in stdout.split('\n\n')]
    if not groups:
        return {}
    group = groups[-2] if len(groups) >= 2 else groups[0]
    cpu_list = [i for i in group.split('\n')]
    cpu_info = {}
    for x in cpu_list:
        if ':' not in x:
            continue
        k, v = [i.strip() for i in x.split(':')]
        cpu_info[k] = v
    return cpu_info


def get_disk_info():
    ret = []
    cmd = r"fdisk -l|egrep '^Disk\s/dev/[a-z]+:\s\w*'"
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    stdout_str = to_unicode(stdout)
    for i in stdout_str.split('\n'):
        disk_info = i.split(",")
        if disk_info[0]:
            ret.append(disk_info[0])
    return ret


def post_data(url, data):
    try:
        headers = {'Content-Type': 'application/json'}
        
        # 如果是相对URL而不是完整URL，则添加协议和服务器地址
        if not url.startswith('http'):
            protocol = 'https' if use_https else 'http'
            url = "{0}://{1}{2}".format(protocol, server_ip, url)
        
        # 添加verify参数控制是否验证SSL证书
        r = requests.post(url, data=data, headers=headers, verify=verify_ssl)
        
        if r.text:
            logging.info(to_unicode(r.text))
        else:
            logging.info("Server return http status code: {0}".format(r.status_code))
    except Exception as msg:
        logging.info(str(msg))
    return True


def asset_info():
    data_info = dict()
    try:
        data_info['memory'] = get_mem_total()
        data_info['disk'] = str(get_disk_info())
        cpuinfo = parser_cpu(get_cpu_model())
        cpucore = get_cpu_cores()
        data_info['cpu_num'] = cpucore['logical']
        data_info['cpu_physical'] = cpucore['physical']
        data_info['cpu_model'] = cpuinfo.get('model name', '')
        data_info['ip'] = get_ip()
        dmi_info = parser_dmi(get_dmi())
        data_info['sn'] = dmi_info.get('Serial Number', '')
        data_info['vendor'] = dmi_info.get('Manufacturer', '')
        data_info['product'] = dmi_info.get('Version', '')
        
        # 处理platform.linux_distribution()在Python 3.8+中的弃用
        try:
            if hasattr(platform, 'linux_distribution'):
                dist = platform.linux_distribution()
            else:
                import distro
                # 使用现代的distro API
                dist = (distro.id(), distro.version(), distro.codename())
            data_info['osver'] = " ".join([dist[0], dist[1], platform.machine()])
        except:
            data_info['osver'] = platform.platform()
            
        data_info['hostname'] = platform.node()
        data_info['token'] = token
        data_info['agent_version'] = AGENT_VERSION
    except Exception as e:
        logging.error("Error collecting asset info: %s", str(e))
    return json.dumps(data_info)


def asset_info_post():
    pversion = platform.python_version()
    pv = re.search(r'2.6', pversion)
    if not pv:
        osenv = os.environ["LANG"]
        os.environ["LANG"] = "us_EN.UTF8"
    logging.info('Get the hardwave infos from host:')
    logging.info(asset_info())
    logging.info('----------------------------------------------------------')
    post_data("/cmdb/collect", asset_info())
    if not pv:
        os.environ["LANG"] = osenv
    return True


def get_sys_cpu():
    sys_cpu = {}
    cpu_time = psutil.cpu_times_percent(interval=1)
    sys_cpu['percent'] = psutil.cpu_percent(interval=1)
    sys_cpu['lcpu_percent'] = psutil.cpu_percent(interval=1, percpu=True)
    sys_cpu['user'] = cpu_time.user
    sys_cpu['nice'] = cpu_time.nice
    sys_cpu['system'] = cpu_time.system
    sys_cpu['idle'] = cpu_time.idle
    sys_cpu['iowait'] = cpu_time.iowait
    sys_cpu['irq'] = cpu_time.irq
    sys_cpu['softirq'] = cpu_time.softirq
    sys_cpu['guest'] = cpu_time.guest
    return sys_cpu


def get_sys_mem():
    sys_mem = {}
    mem = psutil.virtual_memory()
    sys_mem["total"] = mem.total/1024/1024
    sys_mem["percent"] = mem.percent
    sys_mem["available"] = mem.available/1024/1024
    sys_mem["used"] = mem.used/1024/1024
    sys_mem["free"] = mem.free/1024/1024
    sys_mem["buffers"] = mem.buffers/1024/1024
    sys_mem["cached"] = mem.cached/1024/1024
    return sys_mem


def parser_sys_disk(mountpoint):
    partitions_list = {}
    d = psutil.disk_usage(mountpoint)
    partitions_list['mountpoint'] = mountpoint
    partitions_list['total'] = round(d.total/1024/1024/1024.0, 2)
    partitions_list['free'] = round(d.free/1024/1024/1024.0, 2)
    partitions_list['used'] = round(d.used/1024/1024/1024.0, 2)
    partitions_list['percent'] = d.percent
    return partitions_list


def get_sys_disk():
    sys_disk = {}
    partition_info = []
    partitions = psutil.disk_partitions()
    for p in partitions:
        partition_info.append(parser_sys_disk(p.mountpoint))
    sys_disk = partition_info
    return sys_disk


# 函数获取各网卡发送、接收字节数
def get_nic():

    key_info = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称

    recv = {}
    sent = {}

    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数

    return key_info, recv, sent


# 函数计算每秒速率
def get_nic_rate(func):

    key_info, old_recv, old_sent = func()  # 上一秒收集的数据
    time.sleep(1)
    key_info, now_recv, now_sent = func()  # 当前所收集的数据

    net_in = {}
    net_out = {}

    for key in key_info:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  # 每秒接收速率
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024) # 每秒发送速率

    return key_info, net_in, net_out


def get_net_info():
    net_info = []
    key_info, net_in, net_out = get_nic_rate(get_nic)
    for key in key_info:
        in_data = net_in.get(key)
        out_data = net_out.get(key)
        net_info.append({"nic_name": key, "traffic_in": in_data, "traffic_out": out_data})
    return net_info


def agg_sys_info():
    logging.info('Get the system infos from host:')
    sys_info = {'hostname': platform.node(),
                'cpu': get_sys_cpu(),
                'mem': get_sys_mem(),
                'disk': get_sys_disk(),
                'net': get_net_info(),
                'token': token}

    logging.info(sys_info)
    json_data = json.dumps(sys_info)
    logging.info('----------------------------------------------------------')
    post_data("/monitor/received/sys/info/", json_data)
    return True


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def get_pid():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pid = str(os.getpid())
    with open(BASE_DIR+"/adminsetd.pid", "wb+") as pid_file:
        pid_file.write(pid.encode('utf-8'))


def clean_log():
    # 确保目录存在
    log_dir = "/var/opt/adminset"
    log_file = log_dir + "/agent.log"
    
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 清空日志文件
    try:
        with open(log_file, 'w') as f:
            pass  # 只需打开并关闭文件即可清空它
        logging.info("clean agent log")
    except Exception as e:
        logging.error("Failed to clean log: %s", str(e))


if __name__ == "__main__":
    get_pid()
    asset_info_post()
    time.sleep(1)
    #agg_sys_info()
    schedule.every(300).seconds.do(run_threaded, asset_info_post)
    #schedule.every(300).seconds.do(run_threaded, agg_sys_info)
    schedule.every().monday.at("00:20").do(run_threaded, clean_log)
    while True:
        schedule.run_pending()
        time.sleep(1)
