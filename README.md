
# Simulation of Networked non-Markovian Agent Models
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/gerritgr/non-markovian-simulation.svg?branch=master)](https://travis-ci.com/gerritgr/non-markovian-simulation)

Copyright: 2019, Gerrit Großmann, [Group of Modeling and Simulation](https://mosi.uni-saarland.de/) at [Saarland University](http://www.cs.uni-saarland.de/)

Version: 0.1 (Please note that this code is an experimental version in a very early development stage.)
## Overview
------------------
Official code for our paper [Rejection-Based Simulation of Non-Markovian Agents on Complex Networks](https://www.researchgate.net/publication/335841274_Rejection-Based_Simulation_of_Non-Markovian_Agents_on_Complex_Networks). 

## Installation
------------------
Install Julia following the instructions on [https://julialang.org/downloads/platform.html](https://julialang.org/downloads/platform.html). 
Install packages with 
```console
julia setup.jl
```
## Example Usage
-----------------
There is an off-the-shelf script to run the rejection- and baseline-code on all available graph-files:

```console
python evaluation.py
```

Besides, you can run the Julia-code using:

```console
julia sis_reject.jl 10 graph_10k_5p_Infected.txt sis_model_out.txt
```
where `10` is the time horizon and `graph_10k_5p_Infected.txt` is the contact graph (including the initial labeling)
and `sis_model_out.txt` is the name of the output file.
The corresponding rates and rate functions are part of the Julia code.

#### Network File 
The network file contains containing a labeled graph specifying the initial state, each line having the form `<Nodeid>;<Label>;<Neighbor1>,<Neighbor2>,...`
```sh
0;I;31,29,94,13,83
1;S;66,15,73
2;S;29,61,26,80,16,83,30,62,3,93,27,87,68,18,79,6
3;I;83,2,29,4,28,61,46,21,9,49,41,68,16,74
4;S;82,28,12,83,3,62,66,68
...
```
Nodes start with id 0 and are sorted. 
Isolates (nodes withouth neighbors) are not supported (yet). 
There should be at least one node for each possible label. 

##### Output:
TBA

## TODOs
------------------
TBA

## Known Issues and Pitfalls
------------------
TBA

## Runtime Gain Example
------------------
TBA

## More Information
------------------
TBA
