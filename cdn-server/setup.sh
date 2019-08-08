#!/bin/bash +ex

password=`sed -n '1p' /mysql/mysql-secret | base64 -d`
find /home -name 'alembic.ini' | xargs perl -pi -e "s|user:pass|root:$password|g"

cd /home && alembic init alembic
mv /home/env.py /home/alembic/

alembic revision -m "version"

while true;do
    alembic upgrade head
    if [ $? -eq 0 ];then
        break
    else
        sleep 2
    fi
done

python3 /home/main.py
