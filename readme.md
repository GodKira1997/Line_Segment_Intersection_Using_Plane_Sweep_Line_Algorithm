# Assignment 02

This assignment includes 2 python files namely "brute_force.py" & 
"plane_sweep.py", and plane_sweep implmentation also consists the 
visualization of plane sweep on a graph plot through an animation using 
matplotlib.

The plane sweep algorithm implements a custom data structure 
Sweep Line, which is based on a python list implementation. I tried using 
Sorted Set containers (which is implemented using red-black tree), which I 
did use for Event priority queue, but in case of Sweep Line, the comparator 
required to compare the lines in sweep line statues didn't work at the time of swaps. 
So, I implemented the sweep line using list and Event queue using SortedSet.
This implementation is done in sych a way that the list can be easily 
replaced with any other data strcuture and no methods or calls has to changed.

Finally, the visualization is implemented and animated using matplotlib. 
There is a snap of the same in the zip submitted and to see the full 
animation, execute the code with some input file (for eg. datapoints.txt)

## Pre-requisites

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 
libraries (if required).

```bash
pip install sys
pip install Enum
pip install bisect
pip install sortedcontainers
pip install matplotlib
```

## Usage
### For brute_force.py
```commandline
brute_force.py datapoints.txt
```
### For graham_scan.py
```commandline
plane_sweep.py datapoints.txt
```

## Output
The output files are created in the same folder as the python files 
(execution folder).
### For brute_force.py
```markdown
"output_brute_force.txt" file is created and a plot is displayed on execution.
```
### For plane_sweep.py
```markdown
"output_plaen_sweep.txt" file is created and a plot is displayed on execution.
```
