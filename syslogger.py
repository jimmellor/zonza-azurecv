from __future__ import unicode_literals
import logging
import socket
from logging.handlers import SysLogHandler

import settings

class ContextFilter(logging.Filter):
	hostname = socket.gethostname()

	def filter(self, record):
		record.hostname = ContextFilter.hostname
		return True


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

f = ContextFilter()
logger.addFilter(f)

syslog = SysLogHandler(address=(settings.log_svr_addr, settings.log_svr_port))
formatter = logging.Formatter('%(asctime)s {} zonza-azurecv: %(message)s'.format(socket.gethostname()), datefmt=u'%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)