# Pulse Width Modulation - PWD
- PWM is **a technique that uses variable pulse widths** to control power or signal behavior.
- In PWM, the **frequency** is usually fixed, but the **duty cycle changes**.

**Applications:**

1. **LED Brightness**
    - Longer “on” time → brighter LED
    - Shorter “on” time → dimmer LED
2. **Motors**
    - Longer pulses → more power → faster rotation
    - Shorter pulses → less power → slower rotation
3. **Communications Protocols**
    - Encodes data by varying the pulse widths.

> **In IoT / electronics:**  
> PWM allows **DC signals to mimic AC behavior**.

- Example: By turning a DC signal on and off rapidly (high-frequency PWM), I can **control motor speed or simulate voltage levels** without needing complex variable voltage sources.
# Details - Pulse concept and Duty Cycle
In IoT, we often deal with "pulsating DC" that mimics AC behavior for control. 

1. **Square Waves**
    - Think of a square wave like a light switch that turns **on and off repeatedly**.
    - The “on” part is high voltage (1), and the “off” part is low voltage (0).
2. **Pulse Width (PW)**
    - Pulse Width tells me **how long the signal stays “on”** during one cycle.
    - Example: if the pulse is “on” for 0.1 seconds, the PW = 0.1 s.
3. **Period**
    - A **period (T)** is the total time for **one complete on/off cycle**.
    - Example: if the pulse is on for 0.1 s and off for 0.1 s, the total period = 0.1 + 0.1 = 0.2 s.
4. **Frequency**
    - Frequency tells me **how many cycles occur per second**.
    - Formula:
        ```
        f = 1/T
        ```
    - In our example:
        ```
        f = 1 / 0.2 = 5 Hz
        ```
5. **Duty Cycle**
    - Not all square waves are 50/50 on/off.
    - **Duty Cycle (D)** measures the fraction of the period the signal is **on**:
        ```
        D = PW / T
        ```
    - Example: if PW = 0.1 s and T = 0.2 s,
        ```
        D = 0.1 / 0.2 = 0.5 = 50%
        ```
    - This means the signal is “on” half the time, and “off” half the time.
    - If PW were 0.05 s and T = 0.2 s, D = 25% meaning: mostly off, short pulses.

|Parameter|Example Value|Explanation|
|---|---|---|
|Period (T)|0.2 s|Total time for one on/off cycle|
|Pulse Width (PW)|0.1 s|Duration signal is “on”|
|Duty Cycle (D)|50%|PW/T → fraction of time signal is on|
|Frequency (f)|5 Hz|1/T → cycles per second|
If I change **PW** to 0.05 s while keeping T = 0.2 s -> D = 25% -> dimmer LED or slower motor.