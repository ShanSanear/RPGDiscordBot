def flyweight(cls):
    instances = dict()
    return lambda *args, **kwargs: instances.setdefault((args, tuple(kwargs.items())), cls(*args, **kwargs))


class ResourceNotFound(Exception):
    pass


class NotExactMatch(ResourceNotFound):
    pass
