from pprint import pprint
import yaml
import logging
import sys
import os
import re
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from paramiko.ssh_exception import SSHException
from netmiko import (
    ConnectHandler,
    NetMikoTimeoutException,
    NetMikoAuthenticationException,
    NetmikoBaseException,
    ConfigInvalidException
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

# template
template_dir, template_file = os.path.split(sys.argv[1])
vars_file = sys.argv[2]
env = Environment(
    loader=FileSystemLoader(template_dir),
    trim_blocks=True,
    lstrip_blocks=True,
)
template = env.get_template(template_file)

# configuration
def configure_net_devices(device_params, commands):
    try:
        with ConnectHandler(**device_params) as ssh:
            ssh.enable()
            cmd_output = ssh.send_config_set(commands, error_pattern="%")
        return cmd_output
    except ConfigInvalidException:
        raise
    except (NetmikoBaseException, SSHException) as error:
        print(error)


if __name__ == "__main__":
    with open(vars_file) as f:
        vars_dict = yaml.safe_load(f)
    print(template.render(vars_dict))
    r1 = device_list[0]
    result = configure_net_devices(r1, "log 10.1.1.1")
    pprint(result)


===
def send_show(device, show):
    host = device["host"]
    logging.info(f">>>> Connection {host}")
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(show)
        logging.debug(f"<<<< Received {host}\n\n{result}")
    return result

  host = device["host"]
            logger.info(">>>> Connection to {}".format(host))