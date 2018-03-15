# redis-HA
生产环境小规模redisHA方案

（1）为了解决redis单点故障问题，设计了一套方案，防止单台机器宕机，或者redis单个实例崩溃导致服务全部停止；整个自动failover根据配置，可以做到10s以内；

设计思路：
 redis一主两从+ redis sentinel集群 + 脚本（实现vip转移）；
 
 （1）master主机 配置vip 10.10.80.129（对client来说，连接的是10.10.80.129:6379）；
 （2）sentinel 监控redis master， 当发现master服务不可用，自动切换主从，关键步骤：删除原来master主机的vip，新选择的slave->master主机配置相同vip；
 
 对于client来说：10.10.80.129:6379服务只在发生单点故障发生failover时，服务10s不可用，当完成切换后，服务恢复正常，数据完全不丢失，在小规模生产环境中，完全足以支撑业务；

slave 服务器10.10.80.225
![image](https://github.com/jiapengwen/redis-HA/blob/master/images/ip1.jpg)

master服务器10.10.80.35 ，所以会有vip10.10.80.129
![image](https://github.com/jiapengwen/redis-HA/blob/master/images/ip2.jpg)

slave服务器10.10.81.24
![image](https://github.com/jiapengwen/redis-HA/blob/master/images/ip3.jpg)

![image](https://github.com/jiapengwen/redis-HA/blob/master/images/%E9%80%9A%E8%BF%87vip%E8%AE%BF%E9%97%AEredis.jpg)
![image](https://github.com/jiapengwen/redis-HA/blob/master/images/%E9%80%9A%E8%BF%87sentinel%E6%9F%A5%E7%9C%8B%E7%9B%91%E6%8E%A7%E7%9A%84master.jpg)
![image](https://github.com/jiapengwen/redis-HA/blob/master/images/sentinel%E7%9B%91%E6%8E%A7%E6%95%B0%E6%8D%AE.jpg)
