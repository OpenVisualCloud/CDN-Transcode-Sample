
FROM wurstmeister/kafka:2.12-2.4.0

RUN  sed -i 's/\/kafka\/kafka/\/opt\/kafka\/logs\/kafka/' /usr/bin/start-kafka.sh && \
     mkdir /opt/kafka/logs

ARG  UID
ARG  GID
RUN  addgroup -g ${GID} kafka && \
     adduser -D -H -G kafka -g ${GID} -u ${UID} kafka && \
     chown -R kafka:kafka /opt /kafka

USER ${UID}
