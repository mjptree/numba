import numba.unittest_support as unittest
from unittest import loader, case
from os.path import isdir, isfile, join, dirname, basename


class TestLoader(loader.TestLoader):

    # Unfortunately there is right now no other way to set
    # the top-level directory.
    # ('-t' only works after the 'discover' command).
    _top_level_dir = dirname(dirname(dirname(__file__)))

    def _find_tests(self, start_dir, pattern, namespace=False):
        # Upstream doesn't look for 'load_tests' in start_dir.

        if isdir(start_dir) and not namespace and isfile(join(start_dir, '__init__.py')):
            name = self._get_name_from_path(start_dir)
            package = self._get_module_from_name(name)
            load_tests = getattr(package, 'load_tests', None)
            tests = self.loadTestsFromModule(package, use_load_tests=False)
            if load_tests is not None:
                try:
                    yield load_tests(self, tests, pattern)
                except Exception as e:
                    yield loader._make_failed_load_tests(package.__name__, e, self.suiteClass)
        else:
            for t in super(TestLoader, self)._find_tests(start_dir, pattern):
                yield t