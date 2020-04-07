from datetime import datetime
import logging as log
import time
import sys

# logging
log.basicConfig(level=log.INFO,\
  format='%(asctime)s [%(process)d:%(thread)d] %(levelname)s %(pathname)s:%(lineno)d %(message)s')

while True:
  print('stdout: %s' % datetime.now())
  print('outflush: %s' % datetime.now(),flush=True)
  print('stderr: %s' % datetime.now(),file=sys.stderr)
  log.info(datetime.now())
  time.sleep(1)
