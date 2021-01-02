import logging
import sys

LOG_FORMAT='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    stream=sys.stdout
)
