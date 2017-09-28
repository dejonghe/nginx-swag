import json
import logging
import os
from parse import parse
from ruamel.yaml import YAML

from path import Path

logger = logging.getLogger('Common')

yaml = YAML(typ='safe')
yaml.allow_duplicate_keys = True


class Swagger(object):
    def __init__(self, swagger_file):
        self.raw = self._ingest(swagger_file)
        for key, value in self.raw.items():
            setattr(self,key,value)
        if not hasattr(self, 'basePath'):
            setattr(self,'basePath',None)
        self.paths = self._parse_paths()
        #self._amazon_parse()

    def __str__(self):
        return json.dumps(self.raw)

    def yaml(self):
        return yaml.dump(self.__dict__, stdout)

    def _ingest(self, swagger_file):
        with open(swagger_file) as f:
            return yaml.load(f)

    def _parse_paths(self):
        paths = []
        for path, obj in self.raw['paths'].items():
            if self.basePath:
                full_path = "{}/{}".format(self.basePath,path)
                path = re.sub("([^:]\/)\/+", "", full_path)
            paths.append(Path(path,obj))
        return paths

    def _amazon_parse(self):
        for path, obj in self.raw['paths'].items(): 
            if 'x-amazon-apigateway-any-method' in obj: 
                if 'x-amazon-apigateway-integration' in obj['x-amazon-apigateway-any-method']: 
                    if obj['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['type'] == 'aws_proxy': 
                        format_str = "arn:aws:apigateway:{region}:{service}:path/{aws_api_version}/functions/{function}/invocations"
                        uri = obj['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['uri'] 
                        logger.warn(uri)
                        uri_spl = parse(format_str,uri)
                        logger.warn(uri_spl) 
                        self.raw['paths'][path]['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['function'] = uri_spl['function']
