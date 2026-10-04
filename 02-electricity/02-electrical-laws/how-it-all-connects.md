# Summary - how it all connects
- I increase voltage (source), and electrical current increases proportionally (double voltage, double current... assuming constant resistance).
- I decrease voltage (source), and current decreases proportionally.
- If I increase resistance (R) while keeping voltage source (V) constant, the current (I) will decrease (but voltage will drop across resistor in proportion to current).
> So, a voltage drop across a resistor depends on the current flowing through it and its resistance.
- The total **voltage** from the power source remains the same, but because current decreases (due to resistance increase), the voltage drop (amount of energy dissipated by the resistor) also decreases.
> The **power dissipated** by the resistor (in the form of heat) also decreases because power is `P = I^2 * R`, and if the current decreases, the power decreases.

**Water analogy:**  
- Voltage = pump pressure
- Current = water flow
- Resistance = narrow pipe
- Power = water energy delivered per second
- KVL = water pressure lost in pipes = pump pressure
# How it applies
- Always check **current ratings** for wires, traces, and components
- Distribute voltage drops intentionally across resistors, LEDs, motors
- Keep PCB traces sized to handle expected current
- Series components -> same current, sum voltage drops
- Parallel components -> same voltage, current divides
- Always calculate **voltage drop & power** before modifying circuits
- Use **Ohm’s law + KVL/KCL** as first diagnostic tool

## Designing and modifying circuits
- **Ohm’s Law** tells me:
    - What resistor to use to limit current for LEDs, sensors, or microcontrollers
    - What voltage a component will “see” under certain currents
- **KVL** ensures I can predict voltage drops in series circuits -> critical for designing multi-component PCBs

**Example:** I add a new sensor to a board — without checking voltage drops, the sensor might **not get enough voltage to operate reliably**.

## Troubleshooting and repair
- If something isn’t working, knowing **current, voltage, and power relationships** helps me find:
    - **Short circuits** (too much current, possible damage)
    - **Open circuits** (no current, voltage not reaching component)
    - Components overheating because **too much power** is being dissipated

**Example:** A motor on a device keeps burning out -> measuring voltage and current, applying Ohm’s Law, I can **calculate the expected power** and see if the wiring or driver is undersized.

## Ensuring safety and reliability
- Understanding **power = voltage × current** prevents:
    - Burnt traces on PCBs
    - Overheated wires or components
    - Short circuits that could damage devices or cause harm

**Example:** I design a power distribution line for sensors — I need to know **how much current the traces can handle** and what resistors/voltage regulators to use.

## Optimizing performance
- Embedded systems often have **tight energy budgets** (battery-powered devices)
- Knowing electrical laws helps me **minimize energy loss**, maximize efficiency, and size components correctly

**Example:** Choosing a low-resistance path and correct resistor values keeps my device **cooler and battery longer-lasting**.