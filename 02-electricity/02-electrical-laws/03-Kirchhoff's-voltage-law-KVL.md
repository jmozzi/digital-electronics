# Kirchhoff's Voltage Law (KVL): closed loop circuit
- **The sum of all voltage gains and drops around any closed loop is zero**
- In a series loop: voltage gains (battery/source) = sum of voltage drops (resistors, bulbs, etc.)

**Example:**  
- 9 V battery in series with two resistors
    - Resistor 1 drops 5 V (determined by Ohm's law: I × R)
    - Resistor 2 drops the remaining 4 V
- Current is the same throughout the loop
- You **cannot have a voltage drop greater than the source voltage**

> Takeaway: a resistor’s voltage drop is **not fixed**, it depends on the **current flowing through it** (Ohm’s law). KVL ensures all voltage gains are accounted for by drops in the loop.
> **Voltage drop across a resistor depends on current (V = I × R)**


In **normal low-frequency DC/AC circuits**, voltage drops and currents are well-behaved, so KVL is a **very reliable tool**.
Engineers use it to **design circuits, calculate currents, and ensure power distribution works correctly**.

**Use it to:**  
- Check multi-component series circuits
- Diagnose underpowered components
- Verify PCB voltage routing