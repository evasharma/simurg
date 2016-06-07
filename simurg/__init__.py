import logging
import scrapper
from logstash_formatter import LogstashFormatterV2
from simurg import create_corpus

logger = logging.getLogger()
logger.setLevel(logging.INFO)
requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False
handler = logging.StreamHandler()
formatter = LogstashFormatterV2()
handler.setFormatter(formatter)
logger.addHandler(handler)
