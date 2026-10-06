# Safety
The following practical safety steps are taken from the TCM course: https://academy.tcm-sec.com/p/beginner-s-guide-to-iot-and-hardware-hacking
## 1. Work with low voltage (below 30 Volts DC)
Power supply from the mains power (power plug) is 230 V AC, and it gets stepped down to 9 V for our devices.
- why stick to low voltages? 
	- the current is dependent on voltage and resistance:
		- *dry undamaged skin* has pretty high resistance: ca `100kOhm`
		- assume `9 v`, then current is `I` = `9 V / 100 000` = `0.00009` = `0.09 mA`  
			- see Ohm's law [Ohms-law](02-electricity/02-electrical-laws/01-Ohms-law.md)
		- assume `120 V`, then `I` = `120 V/100k Ohm` = `1.2 mA`
		- assume *wet hands/high humidity* and resistance now `1 kOhm`
			- then `I` = `120 / 1 kOhm` = `120 mA` = `0.12A`
- affects on the human body
	- **~1 mA** -> barely perceptible
	- **~5 mA** -> noticeable shock
	- **~10–20 mA** -> muscle control loss (“can’t let go”)
	- **~30–50 mA** -> breathing interference possible
	- **~50–100 mA** -> risk of ventricular fibrillation begins
	- **>100 mA** -> high risk of death, especially with longer exposure

## 2. Only power on circuits when required (otherwise unplug)
## 3. Remove jewellery, as they are good conductors (jewellery can heat up)
## 4. Be mindful of capacitors
see [004-capacitors-filters](10-volatile-memory-DRAM-SRAM/004-capacitors-filters.md)
- they can store electric charge on a circuit
- can build up more powerful charge over time
	- even after circuit is powered off
	- learn how to safely discharge them before working with them
- can be at much higher voltage than rest of circuit operates at
- can get a good shock, possibly dangerous
## ESD - Electrostatic discharge
- avoid shocks due to ES discharge, instead controlled grounding 
- humans can tolerate high voltages (~kV), but small electronic components cannot
	- won't damage them necessarily immediately, but weaken them
- precautions:
	- work on ESD mat (rubber, high surface resistance)
	- discharge yourself before handling components (e.g. touch grounded metal)
	- ESD bags are good for transferring/storing components
	- use an ESD wrist strap
	- we can also ground work area; clip on mat and put it into powerboard GND
		- it will make sure I can't build up static