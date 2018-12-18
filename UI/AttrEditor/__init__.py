from .AWFactory import AWFactory
from .AWPath import AWPath
from .AWLro import AWLro

AWFactory.registerAW(AWPath)
AWFactory.registerAW(AWLro)