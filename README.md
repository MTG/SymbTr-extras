[![Build Status](https://travis-ci.org/MTG/SymbTr-extras.svg?branch=master)](https://travis-ci.org/MTG/SymbTr-extras) [![Code Climate](https://codeclimate.com/github/MTG/SymbTr-extras/badges/gpa.svg)](https://codeclimate.com/github/MTG/SymbTr-extras) [![codecov.io](https://codecov.io/github/MTG/SymbTr-extras/coverage.svg?branch=master)](https://codecov.io/github/MTG/SymbTr-extras?branch=master) [![DOI](https://zenodo.org/badge/52790094.svg)](https://zenodo.org/badge/latestdoi/52790094)

SymbTr-extras
===========
Basic tools to manipulate the SymbTr-scores 

Introduction
------------
This repository hosts a set of tools to validate and manipulate the SymbTr scores and get basic statistics from them. The tools are mostly used for maintaining the [SymbTr repository](https://github.com/MTG/SymbTr) and keeping a track of the stored score metadata and attributes.

If you are using these tools in your work, please cite the dissertation:

> Şentürk, S. (2016). [Computational Analysis of Audio Recordings and Music Scores for the Description and Discovery of Ottoman-Turkish Makam Music](http://sertansenturk.com/research/works/phd-thesis/). PhD thesis, Universitat Pompeu Fabra, Barcelona, Spain.

Usage
------------
Please refer to the interactive demos [apply_extras_txt_file.ipynb](https://github.com/MTG/SymbTr-extras/blob/master/apply_extras_txt_file.ipynb) and [change_symbtr_filename](https://github.com/MTG/SymbTr-extras/blob/master/change_symbtr_filename.ipynb) for the basic usage. To process many documents you can use the [jupyter notebooks](http://jupyter.org/) in the [wrapper](https://github.com/MTG/SymbTr-extras/tree/master/wrappers) folder.

This repository is also used as a submodule in the [SymbTr collection](https://github.com/MTG/SymbTr). For this reason, the paths in the jupyter notebooks are given according to the relative path of the submodule. If you want to use these notebooks outside the submodule, you should change these paths accordingly.

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
