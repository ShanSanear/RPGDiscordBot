def flyweight(cls):
    """
    Flyweight class wrapper.
    :param cls: class to flyweight.
    :return: Check to make sure there are no duplicates of the classes.
    """
    instances = dict()
    return lambda *args, **kwargs: instances.setdefault(
        (args, tuple(kwargs.items())), cls(*args, **kwargs)
    )


class ResourceNotFound(Exception):
    pass


class NotExactMatch(ResourceNotFound):
    pass
