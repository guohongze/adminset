#!/bin/bash
set -e
echo "####stop adminsetd service####"
service adminsetd stop
work_dir=/var/opt/adminset/client
rm -rf $work_dir
os=$(cat /proc/version)
if (echo $os|grep centos) || (echo $os|grep 'Red Hat')
then
    rm -rf /var/lib/systemd/system/adminsetd.service
elif (echo $os|grep Ubuntu)
then
    rm -rf /etc/systemd/system/adminsetd.service
else
    echo "your os version is not supported!"
fi
echo "####admiset agent uninstall finished!####"
