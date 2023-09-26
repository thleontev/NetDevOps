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
    NetmikoBaseException
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
    lstrip_blocks=True
)
template = env.get_template(template_file)

if __name__ == "__main__":
    # load yaml
    with open(vars_file) as f:
        vars_dict = yaml.safe_load(f)
    
    # render template
    config = template.render(vars_dict)
    with open(vars_dict["config_name"],"w", "utf-8") as fc:
        fc.write(config)
    print(config)

