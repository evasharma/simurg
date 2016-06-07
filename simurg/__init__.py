import logging
import scrapper
from logstash_formatter import LogstashFormatterV2

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = LogstashFormatterV2()

handler.setFormatter(formatter)
logger.addHandler(handler)
