import logging, paramiko
from io import StringIO

class NetddLog():
    def __init__(self, name, format="%(asctime)s|%(name)s|%(levelname)s| %(message)s", level=logging.INFO):
        self.name = name
        self.level = level
        self.format = format
        
        # Logger configuration.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)

        self.log_capture_string = StringIO()
        self.ch_logger = logging.StreamHandler(self.log_capture_string)

        self.formatter = logging.Formatter(self.format)
        self.ch_logger.setFormatter(self.formatter)
        self.logger.addHandler(self.ch_logger)
        
        # self.std_logger = logging.StreamHandler()
        # self.std_logger.setFormatter(self.formatter)
        # self.logger.addHandler(self.std_logger)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)
    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)
    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)
    def warning(self, msg, extra=None):
        self.logger.warning(msg, extra=extra)

netdd_logger = NetddLog('Paramiko') #level='INFO'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.set_log_channel('Paramiko')
client.connect('192.168.255.68', username='admin', password='admin', port=22, look_for_keys=False, allow_agent=False)

#print(netdd_logger.log_capture_string.getvalue())
netdd_logger.info("What is going on")
print()
print(netdd_logger.log_capture_string.getvalue().rstrip())