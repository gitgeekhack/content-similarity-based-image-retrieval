def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, importlib.util
    __file__ = pkg_resources.resource_filename(__name__, 'MultiScaleDeformableAttention.cpython-37m-x86_64-linux-gnu.so')
    __loader__ = None; del __bootstrap__, __loader__
__bootstrap__()
