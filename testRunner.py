import unittest

loader = unittest.TestLoader()

tests = loader.discover("tests")

testRunner = unittest.runner.TextTestRunner(verbosity=2)
testRunner.run(tests)
