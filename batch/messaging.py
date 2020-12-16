#!/usr/bin/python3

import socket
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import traceback
import socket
import time

KAFKA_HOSTS = ["kafka-service:9092"]

class Producer(object):
    def __init__(self):
        super(Producer, self).__init__()
        self._client_id = socket.gethostname()
        self._producer = None

    def send(self, topic, message):
        if not self._producer:
            try:
                self._producer = KafkaProducer(bootstrap_servers=KAFKA_HOSTS,
                                               client_id=self._client_id,
                                               api_version=(0, 10), acks=0)
            except:
                print(traceback.format_exc(), flush=True)
                self._producer = None

        try:
            self._producer.send(topic, message.encode('utf-8'))
        except:
            print(traceback.format_exc(), flush=True)

    def flush(self):
        if self._producer:
            self._producer.flush()

    def close(self):
        if self._producer:
            self._producer.close()
            self._producer=None

class Consumer(object):
    def __init__(self, group=None):
        super(Consumer, self).__init__()
        self._client_id = socket.gethostname()
        self._group = group

    def messages(self, topic, timeout=None):
        c = KafkaConsumer(topic, bootstrap_servers=KAFKA_HOSTS, client_id=self._client_id,
                          group_id=self._group, auto_offset_reset="earliest", api_version=(0, 10))

        for msg in c:
            yield msg.value.decode('utf-8')
        c.close()

    def debug(self, topic):
        c = KafkaConsumer(bootstrap_servers=KAFKA_HOSTS, client_id=self._client_id,
                          group_id=None, api_version=(0, 10))

        # assign/subscribe topic
        partitions = c.partitions_for_topic(topic)
        if not partitions:
            raise Exception("Topic "+topic+" not exist")
        c.assign([TopicPartition(topic, p) for p in partitions])

        # seek to beginning if needed
        c.seek_to_beginning()

        # fetch messages
        while True:
            partitions = c.poll(100)
            if partitions:
                for p in partitions:
                    for msg in partitions[p]:
                        yield msg.value.decode('utf-8')
            yield ""

        c.close()
