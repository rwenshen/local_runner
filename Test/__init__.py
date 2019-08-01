import logging
import logging.config

config = {
    'version' : 1,

    'formatters' : {
        'default' : {
            'format' : '%(name)s - %(levelname)s: %(message)s'
        },
    },

    'handlers' : {
        'null' : {
            'class' : 'logging.NullHandler'
        },
        'cd' : {
            'class' : 'logging.StreamHandler',
            'level' : logging.DEBUG,
            'formatter' : 'default',
        },
        'ci' : {
            'class' : 'logging.StreamHandler',
            'level' : logging.INFO,
            'formatter' : 'default',
        },
        'cw' : {
            'class' : 'logging.StreamHandler',
            'level' : logging.WARNING,
            'formatter' : 'default',
        },
    },
    
    'loggers' : {
        'lr.core' : {
            'level': logging.DEBUG,
            'handlers': ['cw'],
        },
        'lr.core.commands' : {
            'level' : logging.DEBUG,
            'handlers' : ['ci'],
            'propagate' : False,
        },
    },
}

logging.config.dictConfig(config)

from . import Environments
from . import Args
from . import Commands
from . import Errors
