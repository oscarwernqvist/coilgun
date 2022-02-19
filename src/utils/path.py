from pathlib import Path


def path_path():
	"""Return the directory of this file"""
	return Path(__file__).parent

def project_path():
	"""Return the top path of the project"""
	return path_path() / '..' / '..'

def src_path():
	return project_path() / 'src'

def test_path():
	return project_path() / 'tests'

def defaults_path():
	return project_path() / 'templates' / 'defaults'