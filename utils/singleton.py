

class Singleton(type):

    def __init__(cls, name, bases, kwargs):
        super(Singleton, cls).__init__(name, bases, kwargs)
        cls._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(Singleton, self).__call__(*args, **kwargs)
        return self._instance