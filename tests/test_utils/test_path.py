import pytest

from pathlib import Path
from utils import path as repo_path


@pytest.mark.parametrize(
	"path_from_func",
	[
		repo_path.project_path() / 'tests' / 'test_utils',
		repo_path.src_path() / '..' / 'tests' / 'test_utils',
		repo_path.test_path() / 'test_utils'
	]
)
def test_project_paths(path_from_func):
	assert path_from_func.resolve() == Path(__file__).parent