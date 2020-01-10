# Setup NFS server or client

[TOC]

Setup NFS server or client on master and slave nodes 
-  Note: If there are two or more machines, make sure NFS server is just one, the others install NFS client. 
#### Install the NFS server (master or slave nodes)
        cd CDN-Transcode-Sample/script
        sudo ./nfs_setup.sh
#### Install the NFS Common client(master or slave nodes)
##### Install the NFS Common client on Ubuntu system
        sudo apt-get install nfs-common
##### Install the NFS Common client on CentOS 
		sudo yum install nfs-utils


