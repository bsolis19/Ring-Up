import logging


def logged(class_):
    class_.logger = logging.getLogger(class_.__qualname__)
    return class_
