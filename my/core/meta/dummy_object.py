class DummyObject:
    """Dummy class for replacing existing classes and simulating their behaviour"""

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, item):
        """Returns dummy object instance on requested attribute even if they don't exist"""
        return DummyObject
