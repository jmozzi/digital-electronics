# Passive components
- **Passive components cannot amplify or actively control signals** (no switching, no gain, meaning they can't make a signal "bigger" or "stronger").
- They **don’t need an external power source** to operate.
- Instead, they **dissipate, store, or release energy**.
	- resistors (resistance)
	- capacitors (capacitance)
	- inductor (inductance)
## Summary
- **Resistor:** “Slows things down” (limits current)
- **Capacitor:** “Buffers voltage” (fills and releases charge)
- **Inductor:** “Buffers current” (resists sudden current changes)
## Resistors (Resistance, R)
- **Function:** Limit current and drop voltage (Ohm’s Law: V=IxR).
- **Energy behavior:** Dissipate energy as heat.

### Common uses:  
- **Pull-up / pull-down resistors (IoT):**
    - Ensure a digital input is **not floating** (undefined voltage), see [[05-MOSFET-CMOS-switch]].
    - Example: A button input pin reads stable HIGH/LOW instead of random noise.
- Current limiting (e.g., protecting LEDs).

### Rating:
- **Ohms (Ω)** = how much it resists electricity (coloured stripes or use multimeter)
- **Watts (W)** = how much power (heat) it can survive (usually goes by size)
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

## Capacitors (C)
- **Function:** Store energy in an **electric field**.
- **Key property:** Resist **changes in voltage**.
    - Voltage across a capacitor cannot change instantly.

### Common uses:  
- **Decoupling / bypass capacitors (IoT & CPUs):**
    - Smooth out voltage dips/spikes near microcontrollers.
- Filtering noise from signals.
- Timing circuits (e.g., RC delays).

## Inductors (Inductance, L)
- **Function:** Store energy in a **magnetic field** (caused by current flow).
- **Key property:** Resist **changes in current**.
    - Current through an inductor cannot change instantly.

### Common uses:   
- **Power supplies (computers & IoT devices):**
    - Found in DC-DC converters feeding CPUs and microcontrollers.
    - Help **smooth current delivery**.
- Filters (e.g., removing high-frequency noise).
- Energy storage in switching regulators.

