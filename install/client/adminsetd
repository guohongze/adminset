#!/bin/sh
#
# Simple Redis init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.
# chkconfig: - 85 15
. /etc/init.d/functions

WORK_DIR="/var/opt/adminset/client"
EXEC="$WORK_DIR/venv/bin/python $WORK_DIR/adminset_agent.py"

PIDFILE=$WORK_DIR/adminsetd.pid

start() {
	if [ -f $PIDFILE ]
	then
			echo "$PIDFILE exists, process is already running or crashed"
	else
			echo "Starting Adminset Agent..."
			nohup $EXEC >/dev/null 2>&1 &
	fi
}

stop() {
	if [ ! -f $PIDFILE ]
	then
			echo "$PIDFILE does not exist, process is not running"
	else
			PID=$(cat $PIDFILE)
			echo "Stopping ..."
			kill -9 $PID
			rm -rf $WORK_DIR/adminsetd.pid
			while [ -x /proc/${PID} ]
			do
				echo "Waiting for Adminset Agent to shutdown ..."
				sleep 1
			done
			echo "adminset agent stopped"
	fi
}

restart() {
    stop
    sleep 1
    start
}

case "$1" in
    start)
	start
	;;
    stop)
	stop
        ;;
    status)
	if [ -f $PIDFILE ]
	then
		echo "adminset agent is running....."
	else
		echo "adminset agent is stopped"
	fi
	;;
    restart)
	restart
	;;
    *)
        echo "service status or stop or start"
        ;;
esac
