
## conductors and insulators
### silicon
- `silicon` is an `insulator` as it
	- has *4 `valence` electrons* (remember [[atomic-structure-and-electricity]])
	- when Silicon atoms come together these valence electrons like to pair up tightly, a `crystal lattice`
	- *no free electrons* to move -> `insulator`
	- if we try pass current through it, it won't work --> insulator
![Pasted image 20251106143945](../images/Pasted%20image%2020251106143945.png)
### doping
- if we mix `silicon` with other elements we can change that property 
- and create a `semi-conductor` used to build transistors
- `doping` = introduction of impurities aka other elements
#### N-Type silicon - free electrons
- doping with `Phosporus` - `N-Type silicon`
	- 5 valence electrons
	- so if we mix those in with the Silicon, they fit nicely, but we end up with a few extra *free electrons*
	- now if we add a charge, the free electrons will be attracted *to positive side* of the battery making room for more to follow
	- we've created a current, and it is *moving towards positive voltages*
- N-Type silicon has `electrons` as majority carriers
![Pasted image 20251106144217](../images/Pasted%20image%2020251106144217.png)
#### P-Type silicon - electron holes
- now we add `Boron`
	- 3 valence electrons
	- it also fits right in, but now we don't have an extra electron, we miss some, we have *holes*
	- aka we created spots where electrons could be 
	- and when we add a current electrons will move to fill nearby holes (not going to positive, but to fill the holes and hence holes appear to move in the opposite direction)
	- a hole behaves like a positive charge; and in P-type material, current appears to flow because holes move towards the negative terminal
- P-Type has `holes` as majority carriers
![Pasted image 20251106144718](../images/Pasted%20image%2020251106144718.png)

# Usage
- **N-type:**
    - Extra electrons → current via electrons
    - Likes **positive voltage**
    - Used for “pull-down” (connect to ground)
- **P-type:**
    - Missing electrons (holes) → current via holes
    - Likes **negative voltage**
    - Used for “pull-up” (connect to Vcc)
see [[05-MOSFET-CMOS-switch]]