# HadHadFakeUncert
## Dependencies
* ROOT
* python 2.6.6 or higher

## Usage
* Setup
```
cd HadHadFakeUncert; source setup.sh
```
* First usage
```
fix-file /path/to/rootfile.root
```
* Rerun
```
fix-file /path/to/rootfile.root --reset
```
* Note

The binay `fix-file` can be use in a path-invariant way. You can call it from anywhere else in your code

## Output
The command creates a new file named `faked_rootfile.root` if the root file is called `rootfile.root`. This new file is created in the 
same directory as the old one.
This output contains four additional histograms for each category:
* 2 variations for the MC contamination
* 2 variatons for the nOS to OS extrapolation
