SymbTr-extras
===========
Basic tools to manipulate the SymbTr-scores 

Introduction
------------
This repository hosts a set of tools to validate and manipulate the SymbTr scores and get basic statistics from them. The tools are mostly used for maintaining the [SymbTr repository](https://github.com/MTG/SymbTr) and keeping a track of the stored score metadata and 
attributes.

Usage
------------
Please refer to the ineractive demos [apply_extras_txt_file.ipynb](https://github.com/MTG/SymbTr-extras/blob/master/apply_extras_txt_file.ipynb) and [change_symbtr_filename](https://github.com/MTG/SymbTr-extras/blob/master/change_symbtr_filename.ipynb) for the basic usage. To process many documents you can use the jupyter notebook files in the [wrapper](https://github.com/MTG/SymbTr-extras/tree/master/wrappers) folder.

This repository is also used as a submodule in the [SymbTr repository](https://github.com/MTG/SymbTr). For this reason the paths in the jupyter notebooks are given according to the relative path of the submodule. f you want to use these notebooks outside the submodule, you can should change these paths accordingly.

Installation
------------
If you want to install the package, it is recommended to install it and all the dependencies into a virtualenv. In the terminal, do the following:

    virtualenv env
    source env/bin/activate
    python setup.py install

If you want to be able to edit files and have the changes be reflected, then
install the repository like this instead:

    pip install -e .

Now you can install the rest of the dependencies:

    pip install -r requirements

Authors
-------
Sertan Senturk
contact@sertansenturk.com

Reference
-------
Thesis
