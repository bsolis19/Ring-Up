import logging
import sys
logging.basicConfig( stream=sys.stderr, level=logging.DEBUG)


def logged(class_):
    class_.logger = logging.getLogger(class_.__qualname__)
    return class_
