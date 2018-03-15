#! /bin/bash
_DEBUG="on" #当DEBUG=on这个字段的时候就会记录日志
DEBUGFILE=/home/wjp/redis_sentinel/sentinel_failover.log
VIP='10.10.80.129'
MASTERIP=${6}
MASK='16'
IFACE='eth0'
#自动检测当前主机地址通过过滤的办法
#MYIP=$(ip -4 -o addr show dev ${IFACE}| grep -v secondary| awk '{split($4,a,"/");print a[1]}')
MYIP='10.10.80.35'

DEBUG () {
if [ "$_DEBUG" = "on" ]; then
echo `$@` >> ${DEBUGFILE}
fi
}
 
set -e
DEBUG date
DEBUG echo $@
DEBUG echo "Master: ${MASTERIP} My IP: ${MYIP}"
if [[ ${MASTERIP} = ${MYIP} ]]; then
if [ $(ip addr show ${IFACE} | grep ${VIP} | wc -l) = 0 ]; then
sudo /sbin/ip addr add ${VIP}/${MASK} dev ${IFACE}
DEBUG date
DEBUG echo "/sbin/ip addr add ${VIP}/${MASK} dev ${IFACE}"
DEBUG date
DEBUG echo "IP Arp cleaning: /usr/sbin/arping -q -f -c 1 -A ${VIP} -I ${IFACE}"
sudo /usr/sbin/arping -q -f -c 1 -A ${VIP} -I ${IFACE}
DEBUG date
DEBUG echo "IP Failover finished!"
fi
exit 0
else
if [ $(ip addr show ${IFACE} | grep ${VIP} | wc -l) != 0 ]; then
sudo /sbin/ip addr del ${VIP}/${MASK} dev ${IFACE}
DEBUG echo "/sbin/ip addr del ${VIP}/${MASK} dev ${IFACE}"
fi
exit 0
fi
exit 1
