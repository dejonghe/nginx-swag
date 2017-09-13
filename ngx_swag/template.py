import os
import logging
from jinja2 import Environment, FileSystemLoader, PackageLoader

logger = logging.getLogger('Common')

class Template(object):
    def __init__(self,template_file):
        self.template_file = template_file
        self.template_env = Environment(
            autoescape=False, 
            loader=PackageLoader('ngx_swag', 'templates'),
            trim_blocks=False)

    def render(self, context):
        return self.template_env.get_template('server.jinja').render(context)
