import os
import unittest

def runAllTests():
	loader = unittest.TestLoader()
	dirname = os.path.dirname(__file__)
	suite = loader.discover(dirname)
	runner = unittest.TextTestRunner()
	runner.run(suite)

def main():
	runAllTests()

if __name__ == "__main__":
	main()
