# Passive components
- **Passive components cannot amplify or actively control signals** (no switching, no gain, meaning they can't make a signal "bigger" or "stronger").
- They **don’t need an external power source** to operate.
- Instead, they **dissipate, store, or release energy**.
	- resistors (resistance)
	- capacitors (capacitance)
	- inductor (inductance)

## Resistors (Resistance, R)
- **Function:** Limit current and drop voltage (Ohm’s Law: V=IxR).
- **Energy behavior:** Dissipate energy as heat.

**Common uses:**  
- **Pull-up / pull-down resistors (IoT):**
    - Ensure a digital input is **not floating** (undefined voltage), see [[05-MOSFET-CMOS-switch]].
    - Example: A button input pin reads stable HIGH/LOW instead of random noise.
- Current limiting (e.g., protecting LEDs).

## Capacitors (C)
- **Function:** Store energy in an **electric field**.
- **Key property:** Resist **changes in voltage**.
    - Voltage across a capacitor cannot change instantly.

**Common uses:**  
- **Decoupling / bypass capacitors (IoT & CPUs):**
    - Smooth out voltage dips/spikes near microcontrollers.
- Filtering noise from signals.
- Timing circuits (e.g., RC delays).

## Inductors (Inductance, L)
- **Function:** Store energy in a **magnetic field** (caused by current flow).
- **Key property:** Resist **changes in current**.
    - Current through an inductor cannot change instantly.

**Common uses:**  
- **Power supplies (computers & IoT devices):**
    - Found in DC-DC converters feeding CPUs and microcontrollers.
    - Help **smooth current delivery**.
- Filters (e.g., removing high-frequency noise).
- Energy storage in switching regulators.

## Summary
- **Resistor:** “Slows things down” (limits current)
- **Capacitor:** “Buffers voltage” (fills and releases charge)
- **Inductor:** “Buffers current” (resists sudden current changes)