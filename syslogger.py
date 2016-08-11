import logging
import socket
from logging.handlers import SysLogHandler

import settings

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

syslog = SysLogHandler(address=(settings.log_svr_addr, settings.log_svr_port))
formatter = logging.Formatter('%(asctime)s {} zonza-azurecv: %(message)s'.format(socket.gethostname()), datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)