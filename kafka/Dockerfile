
FROM wurstmeister/kafka:2.12-2.4.0

RUN  sed -i 's/\/kafka\/kafka/\/opt\/kafka\/logs\/kafka/' /usr/bin/start-kafka.sh && \
     mkdir /opt/kafka/logs

RUN  addgroup kafka && \
     adduser -D -H -G kafka kafka && \
     chown -R kafka:kafka /opt /kafka

USER kafka
