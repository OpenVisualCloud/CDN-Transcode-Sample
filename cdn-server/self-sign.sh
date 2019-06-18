#!/bin/bash -e

if [ ! -d "/var/run/secrets" ];then
    mkdir -p /var/run/secrets
fi

openssl req -x509 -nodes -days 30 -newkey rsa:4096 -keyout /var/run/secrets/self.key -out /var/run/secrets/self.crt << EOL
CN
SH
Shanghai
Zizhu
Data Center Group
Intel Corporation
$1
nobody@intel.com
EOL
chmod 640 "/var/run/secrets/self.key"
chmod 644 "/var/run/secrets/self.crt"
openssl dhparam -dsaparam -out /var/run/secrets/dhparam.pem 4096
chmod 644 "/var/run/secrets/dhparam.pem"
