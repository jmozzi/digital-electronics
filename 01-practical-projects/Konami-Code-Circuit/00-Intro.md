# Konami breadboard project

This project attempts to build a **physical** copy of the classic Konami code sequence (↑↑↓↓←→←→BA) on a breadboard: **direction + A/B + reset** buttons, wired to a **Raspberry Pi** GPIO. The Pi runs Python that watches button presses, checks them against the sequence, and drives **two LEDs** for right/wrong feedback. When the full code is entered correctly, the project shows a simple **“k0n4m164 :) Hire Me!”** fullscreen message on a desktop session.
It is a small end-to-end path from **power and wires** to **logic in code**, with notes.

## What I learnt

- **Raspberry Pi and breadboard wiring** 
	- tying the Pi’s **GND** (and when needed **3.3 V**) to the rails, routing GPIO wires, and using [pinout](https://pinout.xyz/) / BCM (Broadcom SoC Channel) numbering so software identifies GPIO pins on a Raspberry Pi based on the specific Broadcom processor chip, rather than their physical location.
- **Pull-up and pull-down, in software and on the board** 
	- why a floating input is bad; how **internal** pull-ups in code compare to **external** resistors on the breadboard; same **active-low** button idea in both cases. (General theory: [04-pull-up-pull-down-resistor](../../04-transistors/04-pull-up-pull-down-resistor.md).)
- **Inputs and outputs** 
	- **Buttons**: mechanical contacts, typical 4-pin tact layout, one logical press per tap. 
	- **LEDs**: anode/cathode, series resistor, driving a load from a GPIO **output** vs reading a switch on an **input**.
- **Debouncing** 
	- contact **bounce** / chatter, why a tight loop lies; fixing it with **waits**, **re-checks**, and **release-before-next-press** in software ([05-Debouncing](05-Debouncing.md)).
- **BCM vs physical** pin names; 
	- **polling** inputs (e.g. `lgpio.gpio_read`, `Button.is_pressed`, or `GPIO.input`) and how that differs from interrupt-driven edge detection; 
	- **matching a sequence** with a sliding window and **prefix** checks; 
- optional **Tk** fullscreen when a display exists; 
- **GPIO libraries**: **lgpio** (chip open/close, recommended script), **gpiozero**, or **RPi.GPIO** setup/cleanup; **safe limits** (e.g. **no 5 V on GPIO**).

Notes are sorted as per below list. The **Python** programs are not numbered so they can be run with shorter commands.

|  Order | File                                                      | What it is                                                            |
| -----: | --------------------------------------------------------- | --------------------------------------------------------------------- |
| **00** | This note                                                 | Intro + how the docs fit together                                     |
| **01** | [01-Prep-Raspberry-Pi](01-Prep-Raspberry-Pi.md)           | Flash OS, first boot, desktop/SSH                                     |
| **02** | [02-GPIO-Pin-Locations](02-GPIO-Pin-Locations.md)         | Physical header ↔ BCM names (reference)                               |
| **03** | [03-Wiring-Hardware](03-Wiring-Hardware.md)               | Parts, breadboard layout, internal vs external pull-ups, run commands |
| **04a** | [04a-Explain-Py-Code-lgpio](04a-Explain-Py-Code-lgpio.md) | Walkthrough — **lgpio** script (**main / recommended**)               |
| **04b** | [04b-Explain-Py-Code-gpiozero](04b-Explain-Py-Code-gpiozero.md) | Walkthrough — **gpiozero** script                                 |
| **04c** | [04c-Explain-Py-Code-rpigpio](04c-Explain-Py-Code-rpigpio.md) | Walkthrough — **RPi.GPIO** script (legacy)                            |
| **05** | [05-Debouncing](05-Debouncing.md)                         | Bounce, edges, polling vs interrupts (goes with **04a–04c**)           |
| **06** | [06-rpigpio-lgpio-gpiozero](06-rpigpio-lgpio-gpiozero.md) | Why multiple GPIO libraries; differences on newer kernels             |
| **07** | [07-Demonstration](07-Demonstration.md)                   | Demo / build photos (placeholder)                                     |
| **08** | [08-Sources](08-Sources.md)                               | External links / videos                                               |

**Programs** - various versions of the same code using different GPIO libraries:

- [Konami-Code-internal-pull-up-lgpio.py](Konami-Code-internal-pull-up-lgpio.py): **lgpio** matches current Pi OS / kernels.
- [Konami-Code-internal-pull-up-gpiozero.py](Konami-Code-internal-pull-up-gpiozero.py): same behavior with **gpiozero**.
- [Konami-internal-pull-up-rpigpio.py](Konami-internal-pull-up-rpigpio.py): internal pull-ups (`PUD_UP`) with **RPi.GPIO** (legacy).
- [Konami-external-pull-up-rpigpio.py](Konami-external-pull-up-rpigpio.py): external ~10 kΩ pull-ups on the breadboard (`PUD_OFF`) with **RPi.GPIO** (legacy).
