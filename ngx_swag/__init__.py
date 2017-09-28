#!/usr/bin/env python

import os
import sys
import argparse 
import pkgutil

from swag import Swagger
from template import Template

from logger import logger

__version__ = "0.0.1"

'''
Entry point for ngx-swag.
'''

def main():
    #default_template = pkgutil.get_data('ngx_swag', 'templates/server.jinja')
    default_template = os.path.join(os.path.dirname(sys.modules['ngx_swag'].__file__), "templates/server.jinja")
    logger.warn(default_template)
    parser = argparse.ArgumentParser(description='Converts Swagger to NGINX')
    parser.add_argument('swag_file', type=str, help='Swagger File to convert')
    parser.add_argument('-t', '--template', type=str, default=default_template, help='jinja2 template file to use for NGINX config')

    args = parser.parse_args()

    swag = Swagger(args.swag_file)
    template = Template(args.template)

    logger.warn(template.render({"swag":swag}))
    #print(swag.yaml())


if __name__ == '__main__':
    exit = main()
    if exit:
        sys.exit(exit) 
