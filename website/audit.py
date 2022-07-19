import logging
import os

class CustomError(Exception):
    pass

class Audit(CustomError):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.loggingLevel = os.environ.get('LOG_LEVEL', logging.DEBUG)
    
    def info(self, statement):
        self.logger.info(str(statement))
    
    def debug(self, statement):
        if self.loggingLevel == 'DEBUG':
            self.logger.debug(str(statement))

    def warn(self, statement):
        if self.loggingLevel == 'WARN':
            self.logger.warn(str(statement))

    def error(self, statement):
        self.logger.error(str(statement))
    
    def setLogLevel(self, level):
        level = level.upper()
        if level == 'INFO':
            self.loggingLevel = logging.INFO
            os.environ['LOG_LEVEL'] = 'INFO'
        elif level == 'DEBUG':
            self.loggingLevel = logging.DEBUG
            os.environ['LOG_LEVEL'] = 'DEBUG'
        elif level == 'WARN':
            self.loggingLevel = logging.WARN
            os.environ['LOG_LEVEL'] = 'WARN'
        elif level == 'ERROR':
            self.loggingLevel = logging.ERROR
            os.environ['LOG_LEVEL'] = 'ERROR'
    
    def raiseCustomError(msg):
        raise CustomError(msg)