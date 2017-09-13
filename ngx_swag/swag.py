import os
import logging
from parse import parse
from ruamel import yaml

logger = logging.getLogger('Common')

class Swagger(object):
    def __init__(self, swagger_file):
        self.swag = self._ingest(swagger_file)
        self._amazon_parse()

    def _ingest(self, swagger_file):
        with open(swagger_file) as f:
            return yaml.safe_load(f)


    def _amazon_parse(self):
        for path, obj in self.swag['paths'].items(): 
            if 'x-amazon-apigateway-any-method' in obj: 
                if 'x-amazon-apigateway-integration' in obj['x-amazon-apigateway-any-method']: 
                    if obj['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['type'] == 'aws_proxy': 
                        format_str = "arn:aws:apigateway:{region}:{service}:path/{aws_api_version}/functions/{function}/invocations"
                        uri = obj['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['uri'] 
                        logger.warn(uri)
                        uri_spl = parse(format_str,uri)
                        logger.warn(uri_spl) 
                        self.swag['paths'][path]['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['function'] = uri_spl['function']
