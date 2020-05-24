# 5GPy

---

## Dependencies

5GPy runs with Python >= 3.6.9

Install dependecies with

`pip install -r requirements.txt`

## Running the simulation

All simulation configurations must be put at:

`configurations.xml`

The initialization of a simulation is done at:

`simulation.py`

To run a simulation, execute:

`python3 simulation.py`


## Structure

The classes representing the network topology elements are within:

`network.py`

Utility methods can be found and must be places at:

`utility.py`


## Cite

Please, when using 5GPy in your paper, thesis or dissertation, it is mandatory to cite the following reference:

```latex
@article{tinini20195gpy,
title={5GPy: A SimPy-based simulator for performance evaluations in 5G hybrid Cloud-Fog RAN architectures},
author={Tinini, Rodrigo Izidoro and dos Santos, Matias Rom{\'a}rio Pinheiro and Figueiredo, Gustavo Bittencourt and Batista, Daniel Mac{\^e}do},
journal={Simulation Modelling Practice and Theory},
pages={102030},
year={2019},
publisher={Elsevier}
}
```

If you have any questions, please contact me at: rtinini at ime dot usp dot br
