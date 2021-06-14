import logging
import sys

logging.basicConfig(
        format='[%(asctime)s]:%(levelname)s:%(name)s: %(message)s',
        stream=sys.stderr,
        level=logging.DEBUG,
    )

def logged(class_):
    class_.logger = logging.getLogger(class_.__qualname__)
    return class_
