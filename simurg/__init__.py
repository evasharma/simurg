import logging
import scrapper
from logstash_formatter import LogstashFormatterV2

logger = logging.getLogger()
requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False
handler = logging.StreamHandler()
formatter = LogstashFormatterV2()
handler.setFormatter(formatter)
logger.addHandler(handler)
