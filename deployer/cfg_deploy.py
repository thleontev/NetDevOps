from pprint import pprint
import yaml
import logging
import sys
import os
import re
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from rich import print as rprint
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
def configure_net_devices(device_params, commands, check_cmd=None, check_str=None):
    try:
        host = device_params["host"]
        logger.info(">>>> Connection to {}".format(host))
        with ConnectHandler(**device_params) as ssh:
            ssh.enable()
            logger.info(">>>> Sending commmand \"{}\" to {}".format(commands, host))
            cmd_output = ssh.send_config_set(commands, error_pattern="%")
            logger.debug("<<<< Received {}{}{}".format(host,"\n",cmd_output))
            if check_cmd and check_str:
                check_output = ssh.send_command(check_cmd)
                if check_str in check_output:
                    rprint("[green]The configuration was successful")
                    logger.debug("<<<< The configuration was successful")
                else:
                    rprint("[red]The configuration was not successful")
                    logger.debug("<<<< The configuration was not successful")
        return cmd_output
    except ConfigInvalidException:
        raise
    except (NetmikoBaseException, SSHException) as error:
        print(error)


if __name__ == "__main__":
    # load yaml
    with open(vars_file) as f:
        vars_dict = yaml.safe_load(f)
    
    # render template
    config = template.render(vars_dict)
    
    #while yaml device
    #while commands

    r1 = device_list[0]
    result = configure_net_devices(r1, "log 10.1.1.1")
    pprint(result)