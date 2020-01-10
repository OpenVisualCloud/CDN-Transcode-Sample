# Set proxy server(optional)

Configure proxy if your network is restricted as in china

[TOC]



## Configure proxy in Ubuntu system
### Set apt proxy server
Set apt proxy server before run the apt update command once your network is restrict
	

```
gedit /etc/apt/apt.conf
```

Input the following content:
	acquire::http::proxy "http://proxy_server:port";
	acquire::https::proxy "https://proxy_server:port";
	acquire::ftp::proxy "ftp://proxy_server:port";
	acquire::socks::proxy "socks://proxy_server:port";

### Automate Proxy Server Settings using Bash functions as follows (add to your ~/.bashrc file):
	gedit ~/.bashrc
	# Set Proxy
	export http_proxy='http://proxy_server:port'
	export https_proxy='http://proxy_server:port'
Reload your ~/.bashrc file
	

```
source ~/.bashrc
```




## Configure proxy in CentOS
### Configure yum proxy
	sudo vi  /etc/yum.conf
Input the following content:
        proxy=http://proxy_server:port/
        proxy=ftp://proxy_server:port/

### Configure  wget proxy
	sudo vi /etc/wgetrc
Input the following content:
        proxy=http://proxy_server:port/
        proxy=ftp://proxy_server:port/

### Configure the global proxy
	sudo vi  /etc/profile
Input the following content:
        http_proxy=http://cerver:port/
        ftp_proxy=http://proxy_server:port/
        export http_proxy
        export ftp_proxy     
Reload your /etc/profile file

​		

```
source /etc/profile
```

