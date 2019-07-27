#!/bin/bash
#set -ex

password=`sed -n '1p' /mysql/mysql-secret | base64 -d`

service mysql start
mysql <<EOF 2>/dev/null

create database Player;
use mysql;

update user set password=password('$password') where user='root' and host='localhost';
grant all privileges on *.* to 'root'@'%' identified by "$password" with grant option;

use Player;
source /mysql/init.sql;
flush privileges;
exit;

EOF
while [ 1 -le 100 ]
do 
    echo '1'
    sleep 1
done
