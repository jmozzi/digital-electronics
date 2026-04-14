https://au.rs-online.com/web/content/discovery/ideas-and-advice/resistors-guide

## Resistors: 
- managing current flow, 
- dividing voltage, and 
- safeguarding other components from excessive current.  
A resistor impedes the flow of electric current in a circuit.   
How? It creates a *voltage drop proportional to the current flowing through it and its resistance value*  
-> **Ohm's law**: `V = I x R `see [Ohms-law](Ohms-law.md)  
This resistance converts electrical energy into **heat**, effectively controlling the current.
## Properties of resistors
- Resistance R - measured in Ohms: quantifies how strongly the resistor opposes the flow of electrical current.
- Power Rating P - specifies the max amount of power, measured in Watts that it can safely dissipate without overheating or damage. Meaning it's important to chose the correct power rating for a specific use case.
- Tolerance - is the permissible deviation in the actual resistance value from what is specified expressed as percentage. Lower tolerance values are more precise: a 1kΩ resistor with a 1% tolerance will have an actual resistance value between 990Ω and 1010Ω.
- Temp coefficient - indicates how much a resistor's resistance changes in response to temperature fluctuations. Important for use cases with big temperature fluctuations, such as automotive electronics or industrial control systems. A positive temperature coefficient means the resistance increases with temperature, while a negative coefficient means it decreases.
## Materials for resistors
- Carbon film resistors:
	- affordable, suitable for general-purpose uses
- Metal film resistors:
	- stability and lower noise levels, suitable for precision 
- Wire-wound:
	- designed for high-power uses

## Types of resistors
### Fixed resistor
- Predetermined, unchangeable resistance value.
- Commonly used for current limiting, voltage division, and setting bias points for transistors.
- Available in various sizes, power ratings, and tolerance levels.
![screenshot](../../images/Pasted%20image%2020260402092158.png)


### Variable resistor
- Also called `potentiometer` or `rheostats`.
- Allow for manual adjustment of resistance value.
- Used for volume control, light dimmers, and sensor calibration.

![](../../images/Pasted%20image%2020260402093257.png)
### Specialty resistor
- **Thermistors**: 


![](../../images/Pasted%20image%2020260402093313.png)


- Ohm's law and resistors
- what does a resistor do
	- current limiting
	- voltage divider
	- biasing transistors
	- signal processing (filter or amplify signals; shape or condition signals (audio))
	- power dissipation
- Resistor value markings
	- colour code system
	- alphanumeric marking for surface mount resistors (SMD)

![screenshot](../../images/Pasted%20image%2020260401143507.png)


### Resistance value
The resistance value, measured in Ohm, can be seen by the coloured stripes of a resistor:
- First 2–3 bands = numbers
- Next band = multiplier
- Last band = tolerance (accuracy)
It goes like this:
- look for the starting end: Look for the **tolerance band** (usually:
	- gold = ±5%
	- silver = ±10%)
	- -> That band is **at the end**, so read from the opposite side.
- Pattern of a 4-band resistor:
	- `[digit] [digit] × [multiplier] (tolerance)`
- Example: Brown-Black-Red-Gold
	- Brown = 1, Black = 0 ... that gives 10
	- Red means multiply by 10 ... that is 10 × 100 = **1000 Ω (1 kΩ)**
	- Gold = ±5% (tolerance)

**Digit Colours:**

|Colour|Number|
|---|---|
|Black|0|
|Brown|1|
|Red|2|
|Orange|3|
|Yellow|4|
|Green|5|
|Blue|6|
|Violet|7|
|Grey|8|
|White|9|
### Power rating
This is the **maximum power the resistor can safely handle** before burning out. Unlike resistance, it’s usually judged by **physical size**:

Typical sizes:
- Small (≈6 mm) → **0.25 W (¼ watt)**
- Medium → **0.5 W (½ watt)**
- Bigger → **1 W or more**



# Calculation Example
9V battery
green LED (can handle max 3.2V)
breadboard, no other information

1st step: subtract LED voltage from supply to see what Voltage the resistor would have to deal with
9V - 3.2V = 5.8 V

2nd: assume a resistor value, e.g. 1000 Ohm (1kOhm), then the current would be:
I = 5.8 / 1000 = 0.0058A = 5.8mA

--> so, I need to assume a resistor value to be able to calculate what the respective current would be with that resistance

So, can say: green LED, roughtly 3 V:
assume 1kOhm resistor: (9-3) / 1000 = ca 6 mA
assume 330 Ohm resistor: (9-3) / 330 = ca 18 mA
assume 220 Ohm resistor: (9-3) / 220 = 27 mA
but put 2 LEDs in series: (9-6) / 220 = ca 13 mA