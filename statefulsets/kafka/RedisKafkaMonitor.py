#!/usr/bin/env python
# coding=utf-8

import re
import sys
import logging
from config import send_msg
from config import get_redis
from subprocess import Popen, PIPE

logger = logging.getLogger(__file__)

KAFKA_QUEUE_SIZE = 100
REDIS_QUEUE_SIZE = 1000000
SEND_USERS = '@all'

class RedisKafkaMonitor(object):

    def __init__(self):
        self.kafka_cmd = '/opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server'
        self.kafka_addr = sys.argv[1]
        self.consumers = []

    def run(self):
        self.redis_monitor()
        self.kafka_monitor()

    def kafka_monitor(self):
        p = Popen('%s %s --list' % (self.kafka_cmd, self.kafka_addr),
                  shell=True, stdout=PIPE, stderr=PIPE)
        for i in p.stdout.readlines():
            if not re.search('\d|\.', bytes.decode(i)):
                self.consumers.append(bytes.decode(i).strip())
        logger.info(self.consumers)
        for consumer in self.consumers:
            if consumer == 'loanAudit' or consumer == 'reportStatistics':
                continue
            p = Popen('%s %s --describe --group %s' % (self.kafka_cmd,
                                                       self.kafka_addr, consumer), shell=True, stdout=PIPE, stderr=PIPE)
            for i in p.stdout.readlines():
                # [u'user.login.notice.v4', u'1', u'36085', u'47513', u'11428', u'-', u'-', u'-']
                if bytes.decode(i).strip() and not bytes.decode(i).startswith('TOPIC'):
                    line = [j for j in bytes.decode(i).strip().split(' ') if j]
                    logger.info(line)
                    try:
                        if int(line[4]) > int(KAFKA_QUEUE_SIZE):
                            logger.info('consumer:%s, topic:%s, partition:%s, current-offset:%s, logger-end-offset:%s, lag:%s'
                                     % (consumer, line[0], line[1], line[2], line[3], line[4]))
                            msg = u'阿里云消费者: %s，kafka topic: %s， partition: %s，待消费%s条' % (
                                consumer, line[0], line[1], line[4])
                            send_msg(SEND_USERS, msg)
                    except:
                        pass

    def redis_monitor(self):
        r = get_redis()
        nodecount = r.info()['nodecount']
        logger.info(nodecount)
        # for k,v in r.info().items():
        #  logger.info(u'%s %s' %(k,v))
        keyspace_info = r.info('keyspace')
        for db in keyspace_info:
            logger.info('check %s %s' % (db, keyspace_info[db]))
            if nodecount > 1:
                self.find_big_key_sharding(db.replace('db', ''), nodecount)
            else:
                self.find_big_key_normal(db.replace('db', ''))

    def _check_big_key(self, db_num, r, k):
        length = 0
        try:
            type = bytes.decode(r.type(k))
            if type == 'string':
                return
            elif type == 'hash':
                length = r.hlen(k)
            elif type == 'list':
                length = r.llen(k)
            elif type == 'set':
                length = r.scard(k)
            elif type == 'zset':
                length = r.zcard(k)
        except:
            return
        # redis大于100万keys
        if length > REDIS_QUEUE_SIZE:
            mes = u'阿里云Redis: %s，%s，%s，%s' % (db_num, k, type, length)
            logger.info(mes)
            send_msg(SEND_USERS, mes)

    def find_big_key_normal(self, db_num):
        r = get_redis(db_num)
        for k in r.scan_iter(count=100):
            self._check_big_key(db_num, r, k)

    def find_big_key_sharding(self, db_num, nodecount):
        r = get_redis(db_num)
        cursor = 0
        for node in range(0, nodecount):
            while True:
                iscan = r.execute_command('iscan', str(
                    node), str(cursor), 'count', '100')
                for k in iscan[1]:
                    self._check_big_key(db_num, r, k)
                cursor = iscan[0]
                logger.info(u'%s %s %s %s' %
                         (cursor, db_num, node, len(iscan[1])))
                if cursor == '0':
                    break


if __name__ == '__main__':
    RedisKafkaMonitor().run()
