
# LumPy
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/gerritgr/LumPyQest.svg?branch=master)](https://travis-ci.org/gerritgr/LumPyQest)

Copyright: 2018, Gerrit Großmann, [Group of Modeling and Simulation](https://mosi.uni-saarland.de/) at [Saarland University](http://www.cs.uni-saarland.de/)

Version: 0.1 (Please note that this code is an experimental version in a very early development stage.)
## Overview
------------------
The LumPy toolset provides a proof of concept for lumping for AME equations for multistate processes on complex networks.
It reduces the large number of ODEs given by the equation systems by clustering them and only solving a single ODE per cluster.
LumPy is written in Python 3 (requiring SciPy) and published under GPL v3 license.

As input, the tool takes model descriptions (containing degree distribution, rules,
time horizon, etc.) and outputs the lumped (or original) equations in the form of a standalone Python script.
## Installation
------------------
We recommend Python 3.6.
##### Requirements:

Packages can be installed with
```sh
pip install -r requirements.txt
```

## Example Usage
-----------------
Typically, you run LumPy like this
```sh
python ame.py <modelfilepath>
```
which generates a python script (placed in the output folder) and executes it.
Available options are:
```sh
positional arguments:
  model          path to modelfile

optional arguments:
  -h, --help     show this help message and exit
  --noautorun    generate code (i.e. equations) without executing (solving) it
  --nolumping    generate original equations without lumping
  --autolumping  use heuristic to determine number of clusters (ignores cluster number in model spec. file)
```
Optimal arguments overwrite the modelfile specification.
##### Caution:
* The code uses eval and exec, please use with sanitized input only.
* Existing files are overwritten without warning.
##### Output:
Ame.py outputs:

* the generated Python script
* the clustering as .csv file
* the dynamcis as .pdf and .csv
* a visualization of the clustering and the initial distribution (only useful in 2d)

When the heuristic is used to determine cluster number, all intermediate steps are stored.

## Files
------------------
| Filename | Function |
| ------ | ------ |
| ame.py | creates python code for lumped AME equations|
| model_parser.py | parses the model file and returns a dictionary containing model |
| utilities.py | useful functions regarding logging/timing/IO |
| cluster_engine.py | implements clustering for a given number of clusters for AME|
| evaluation.py | only used for evaluation purposes and to generate plots |
| expr_generator.py | generates AME formulas |


## Model Descriptions
-----------------
The .yml model files (placed in the model directory by default) specifies the multistate process, the network, initial fractions, the number of bins, etc. An example SIR model file contains:
```
rule:  
  - S -> I: 3.0*I       #contact rule, "3.0*I" means three times number of infected neighbors
  - I -> R: 2.0         #independent rules
  - R -> S: 1.0  

horizon: 5
eval_points: 101 #optional, default 1001, splits the interval 0..<horizon> into <eval_points> points at which stats are reported.

initial_distribution:
  S: 2.0         #automatic normalization, cannot be zero
  I: 1.0
  R: 1.0

network:    
  kmax: 60  #maximal degree in network, minimal degree not supported so far
  degree_distribution: k**(-3.0) if k > 0 else 0.00001  #automatic truncation (at kmax) and normalization
lumping:
  degree_cluster: 15  
  proportionality_cluster: 15

```

## TODOs
------------------
*  Output C++ code instead of Python
*  Use symbolic expressions (not strings) consequently during code generation
*  Stop using dicts in AME solver and delete unused betas
*  Refactor/clean/document code

## Known Issues and Pitfalls
------------------
* Underflows:
  Due to the size of the steps of the ODE solver, an ODE which converges to
  zero might become zero (or less than zero) and cause numerical problems.
  We solve this by truncating these values.


## SIR Example
------------------
![Example](https://i.imgur.com/wQuYG21.png)

## More Information
------------------
on Lumping:

* Kyriakopoulos et al.
["Lumping of Degree Based Mean Field and Pair Approximation Equations for Multi-State Contact Processes"](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.97.012301)
*  G. Großmann et al.
["Lumping the Approximate Master Equation for Multistate Processes on Complex Networks"](https://arxiv.org/abs/1804.02981)
* G. Großmann
"Lumping the Approximate Master Equation for Stochastic Processes on Complex Networks" (Master's thesis)

on AME:

* JP Gleeson
["High-accuracy approximation of binary-state dynamics on networks"](https://arxiv.org/pdf/1104.1537.pdf)

![LSP](http://25.media.tumblr.com/tumblr_mdwcwsB9Ji1rl3jgdo1_500.gif)
