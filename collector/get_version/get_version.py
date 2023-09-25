# Python 3.5
'''
!!! Add your credentials for access to network devices !!!
cd ~
vi .bash_profile
export SSH_USERNAME="username"
export SSH_PASSWORD="password"
export SSH_ENABLE_PASSWORD="password"
source .bash_profile
'''

from pprint import pprint
import yaml
import logging
import os
import re
from paramiko.ssh_exception import SSHException
from netmiko import (
    ConnectHandler,
    NetMikoTimeoutException,
    NetMikoAuthenticationException,
)

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # NOSET,INFO,DEBUG

logfile = logging.FileHandler('logfile.log')
logfile.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%H:%M:%S')
logfile.setFormatter(formatter)
logger.addHandler(logfile)

# regex
version_pattern = re.compile(r'Cisco .+ Software .+ Version (\S+),') 
image_pattern = re.compile(r'image file is "flash.*:(\S+)"')

def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            host = device["host"]
            logger.info(">>>> Connection to {}".format(host))
            ssh.enable()
            for command in commands:
                logger.info(">>>> Sending commmand \"{}\" to {}".format(command, host))
                output = ssh.send_command(command)
                result[command] = output
                logger.debug("<<<< Received {}{}{}".format(host,"\n",result))
        return result
    except (NetMikoTimeoutException, NetMikoAuthenticationException, SSHException) as error:
        print(error)


if __name__ == "__main__":
    user = os.environ.get("SSH_USERNAME")
    passwd = os.environ.get("SSH_PASSWORD")
    enable = os.environ.get("SSH_ENABLE_PASSWORD")

    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    print("==========")
    for device in devices:
        device = {**device, "username": user, "password": passwd, "secret": enable}
        result = send_show_command(device, ["show version"])
        # pprint(result, width=120)
        version_match = version_pattern.search(result["show version"])
        image_match = image_pattern.search(result["show version"])
        print(device["host"],version_match.group(1), image_match.group(1).replace("/",""))
        
    print("==========")

