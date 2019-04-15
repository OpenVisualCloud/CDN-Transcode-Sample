#!/bin/bash -e

if [ ! -d "/run/secrets" ];then
    mkdir -p /run/secrets
fi

openssl req -x509 -nodes -days 30 -newkey rsa:4096 -keyout /run/secrets/self.key -out /run/secrets/self.crt << EOL
SH
SH
Shanghai
Zizhu
Data Center Group
Intel Corporation
$1
nobody@intel.com
EOL
chmod 640 "/run/secrets/self.key"
chmod 644 "/run/secrets/self.crt"
openssl dhparam -dsaparam -out /run/secrets/dhparam.pem 4096
chmod 644 "/run/secrets/dhparam.pem"
