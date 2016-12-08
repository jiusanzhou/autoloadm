"""
Auto load module from sub directory
"""

__title__ = 'autoLoad'
__version__ = '0.1.1'
__author__ = 'John Zoe'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 John Zoe'

def loadM(src="m", start_with="_m_", end_with=".py", index_func="main", set_globals=[], graceful=False, *args, **kwargs):
    """
    Load module index from directory.
    :param src, target directory
    :param startswith, module file should start with this and ends with '.py'
    :param index_func, use this function to access this module
    :param set_globals, set to module can use
    :return {} index_func dict, module_name -> index_func
    """
    import os
    # get module from each file
    _ = map(lambda _: __import__("{0}.{1}".format(src, _[:-1*len(end_with)]), fromlist=[index_func]), 
        filter(lambda _: _.startswith(start_with) and _.endswith(end_with), os.listdir(src) if os.path.isdir(src) else []))
    # filt if index_func not in target m
    __ = filter(lambda _: hasattr(_, index_func), _)
    # set set_globals to each module
    map(lambda _: map(lambda __: setattr(_, __, globals()[__]), filter(lambda _: _ in globals(), set_globals)), __)
    if graceful: map(lambda _: map(lambda __: setattr(_, __, None), filter(lambda _: _ not in globals(), set_globals)), __)
    # return each index_func by module name
    return {_.__module__.replace("{0}.{1}".format(src, start_with), ""): _ for _ in map(lambda _: getattr(_, index_func), __)}
    # return map(lambda _: getattr(_, index_func), __)

def _test_loads():
    ms = loadM(set_globals=["A"])
    print(ms)

def _test_graceful():    
    ms = loadM(set_globals=["A", "B"], graceful=True)
    for _, v in ms.items(): v()

def test(start_with="_test_"):
    for _ in filter(lambda _: _.startswith(start_with), globals()): print("--- run test function {0} ---".format(_.replace(start_with, ""))); globals()[_]()

if __name__ == '__main__':
    test()
