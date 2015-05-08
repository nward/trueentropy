import os
import array
import daemon
from time import sleep
import syslog
from subprocess import call
from fcntl import ioctl

RNDGETENTCNT = 2147766784

def get_entropy_count():
  buf = array.array('h', [0])
  random_dev_fd = os.open('/dev/random', os.O_WRONLY)
  ioctl(random_dev_fd, RNDGETENTCNT, buf)
  os.close(random_dev_fd)
  return buf[0]

getentropy_script = os.path.abspath(os.path.dirname(__file__)) + "/getentropy.py"

syslog.openlog('trueentropy')
syslog.syslog('Starting')

with daemon.DaemonContext():
  while True:
    entropy_count = get_entropy_count()
    if entropy_count < 3000:
      syslog.syslog("Entropy is %d, getting some more" % entropy_count)
      call(["python", getentropy_script])
      syslog.syslog("Now we have %d entropy" % get_entropy_count())
    sleep(10)