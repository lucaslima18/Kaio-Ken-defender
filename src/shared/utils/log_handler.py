import logging

import coloredlogs


class LogHandler(coloredlogs.ColoredFormatter):
    def __init__(
        self,
        fmt="[%(levelname)s] - %(asctime)s, [%(name)s] %(message)s",
        level="INFO",
        logger_name=None,
    ):
        self.fmt = fmt
        self.level = level
        self.logger = logging.getLogger(logger_name)
        super().__init__(self.fmt, self.level)
        coloredlogs.install(level=self.level, fmt=self.fmt, logger=self.logger)

    def reset_logger(self):
        self.fmt = "[%(levelname)s] - %(asctime)s, [%(name)s] %(message)s"
        coloredlogs.install(level=self.level, fmt=self.fmt)

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)
