from jinja2 import Environment, FileSystemLoader
import yaml
import sys
import os

# load yaml 
vars_file = sys.argv[1]
with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)

# load template
template_dir, template_file = os.path.split(vars_dict['template'])
env = Environment(
    loader=FileSystemLoader(template_dir),
    trim_blocks=True,
    lstrip_blocks=True)
template = env.get_template(template_file)

# render template
fname = vars_dict['name_file']
with open(fname, 'w', encoding="utf-8") as f:
    f.write(template.render(vars_dict))
    f.close()
print ("File {} saved...".format(fname))