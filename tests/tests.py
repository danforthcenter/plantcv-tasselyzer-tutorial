import os
import shutil
import pytest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

project_root = os.getcwd()
inputs_list = [
    [project_root, 'index.ipynb']
]


# ##########################
# Tests executing the notebook
# ##########################
@pytest.mark.parametrize('dir,notebook', inputs_list)
def test_notebook(dir, notebook, tmpdir):
    tmp = tmpdir.mkdir('sub')
    # Change working directory
    os.chdir(dir)
    # Open the notebook
    with open(notebook, "r") as f:
        nb = nbformat.read(f, as_version=4)

    # Process the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(nb, {"metadata": {"path": dir}})

    # Save the executed notebook
    out_nb = os.path.join(tmp, "executed_notebook.ipynb")
    with open(out_nb, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    assert os.path.exists(out_nb)
