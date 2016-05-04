- ipconfig(internet protocol configuration): 用于Windows操作系统,显示当前所有的TCP/IP网络配置值, 刷新动态主机配置协议(DHCP)和域名设置.不使用参数时,显示ipv4和ipv6的地址,子网掩码和所有适配器的默认网关. 多数情况下,常与`/all`一起使用,以展示更多细节的信息.
https://technet.microsoft.com/en-us/library/bb490921.aspx

- ping: 用于测试数据包能否通过IP协议到达特定主机.其工作原理是向目标主机发送一个ICMP的响应请求包,并等待响应.它依据往返时间和成功响应的次数来估计丢包率与网络延时;(Windows)通过发送ICMP回声请求消息(echo request message)来验证与网络上另一台支持TCP/IP协议族的计算机在IP层的联通性.显示相应的回声应答消息的接收情况与往返时间.ping主要用于诊断连接性,可访问性和域名解析.
https://technet.microsoft.com/en-us/library/bb490968.aspx

- netstat(network statistics): (Linux)打印网络连接,路由表,接口统计信息,伪装连接(masquerade connection);(Windows)显示有效的TCP连接(不指定任何参数时),当前正在监听的端口,以太网统计信息,ip路由表,IPv4统计信息,IPv6统计信息.
https://technet.microsoft.com/en-us/library/bb490938.aspx

- tracert:(Windows)
https://technet.microsoft.com/en-us/library/bb491018.aspx

- arp:(Linux)操纵系统的arp缓存;(Windows)显示并更新arp缓存的条目,arp缓存存有一张或多张表,表中的内容为ip地址与解析得到的以太网或令牌环的物理地址
https://technet.microsoft.com/en-us/library/bb490864.aspx

- telnet:使用telnet协议与远程计算机进行通信
https://technet.microsoft.com/en-us/library/bb491013.aspx

