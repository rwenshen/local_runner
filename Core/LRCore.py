import logging

def getLogger(name:str=''):
    return logging.getLogger(f'lr.core.{name}')
