from logging import DEBUG, INFO, WARN, ERROR, info, warn, error
from cast_common.logger import Logger
from json import load
from argparse import ArgumentParser
from json import JSONDecodeError

__author__ = ["Nevin Kaplan","Shirley Truffier-Blanc"]
__email__ = ["n.kaplan@castsoftware.com,","s.truffier-blanc@castsoftware.com"]
__copyright__ = "Copyright 2022, CAST Software"

class Config(): 
    def __init__(self, config):
        
        #do all required fields contain data
        try:
            with open(config, 'rb') as config_file:
                self._config = load(config_file)
        except JSONDecodeError as e:
            msg = str(e)
            self.error('Configuration file must be in a JSON format')
            exit()
        except ValueError as e:
            msg = str(e)
            self.log.error(msg)
            exit()

    @property
    def Configuration(self):
        return self._config['Configuration']    

    @property
    def database(self):
        return self.Configuration['Database']['database']

    @property
    def user(self):
        return self.Configuration['Database']['user']

    @property
    def password(self):
        return self.Configuration['Database']['password']
    
    @property
    def host(self):
        return self.Configuration['Database']['host']
    
    @property
    def port(self):
        return self.Configuration['Database']['port']
    
    @property
    def template(self):
        return self._config['template']