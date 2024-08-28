import paramiko
from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig
import logging
from pssh.utils import *
from pssh import logger

enable_host_logger()
enable_logger(logger)

logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s',filename='ssh_test/pssh.log', filemode='w')

#running asynchronous SSH commands in parallel 
hosts = ['192.168.254.250', '192.168.255.2']
#Per-Host Configuration
host_config = [
    HostConfig(port=22, user='admin', password='admin'),
    HostConfig(port=22, user='admin', password='admin'),
]

client = ParallelSSHClient(hosts, host_config=host_config)

#Commands are executed concurrently on every host given
cmd = '''
version
'''

output = client.run_command(cmd)

for host_output in output:
    print(f"Host {host_output.host}")    
    for line in host_output.stdout:
        print(line)
