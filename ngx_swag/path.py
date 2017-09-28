import json
import logging
from ruamel import yaml
from itertools import groupby

logger = logging.getLogger('Common')

class Path(object):
    def __init__(self,path,*raw,**kwargs):
        self.path = path
        self.raw = raw
        for dictionary in raw:
          logger.warn(dictionary)
          self.methods = self._get_methods(dictionary)
          for key in dictionary:
            setattr(self,key,dictionary[key])
            logger.warn(dictionary)
        for key in kwargs:
            setattr(self,key,kwargs[key])

    def __str__(self):
        return json.dumps(self.__dict__)
    def yaml(self):
        return yaml.dump(self.__dict__)

    def _get_attrs(self,data):
        return {}

    def _get_methods(self,data):
        methods = []
        for method, obj in data.items():
            methods.append(Method(method,obj))
        return methods
            
class Method(object):
    def __init__(self,method_type,*raw,**kwargs):
        self.type = method_type
        for dictionary in raw:
          for key in dictionary:
            setattr(self,key,dictionary[key])
        for key, value in kwargs.items():
            setattr(self,key,value)

    def __str__(self):
        return json.dumps(self.__dict__)
    def yaml(self):
        return yaml.dump(self.__dict__)
