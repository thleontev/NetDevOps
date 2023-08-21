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

logging.getLogger("paramiko").setLevel(logging.INFO)
logging.getLogger("netmiko").setLevel(logging.INFO)

logging.basicConfig(
    format="{asctime} - {name} - {levelname} - {message}",
    datefmt="%H:%M:%S",
    style="{",
    level=logging.INFOL,
    filename="py_log.log",
    filemode="w"
)

file_handler_info = logging.FileHandler('result_info.log')
file_handler_info.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(SyntaxError)
# stream_handler = logging.StreamHandler(sys.stdout)

# IOS
version_pattern = re.compile(r'Cisco .+ Software .+ Version (\S+),') 
image_pattern = re.compile(r'image file is "flash0:(\S+)"')

def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            host = device["host"]
            logging.info(">>>> Connection ", host)
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
                logging.debug("<<<< Received ", host, "\n\n",result)
        return result
    except (NetMikoTimeoutException, NetMikoAuthenticationException, SSHException) as error:
        print(error)


if __name__ == "__main__":
    user = os.environ.get("SSH_USERNAME")
    passwd = os.environ.get("SSH_PASSWORD")
    enable = os.environ.get("SSH_ENABLE_PASSWORD")

    with open("devices_envvar.yaml") as f:
        devices = yaml.safe_load(f)

    for device in devices:
        device = {**device, "username": user, "password": passwd, "secret": enable}
        result = send_show_command(device, ["show version"])
        # pprint(result, width=120)
        print("==========")
        version_match = version_pattern.search(result["show version"])
        image_match = image_pattern.search(result["show version"])
        print(version_match.group(1), "\n", image_match.group(1))
        print("==========")

