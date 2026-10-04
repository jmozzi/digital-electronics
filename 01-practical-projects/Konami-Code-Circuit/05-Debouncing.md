# Debouncing (and related ideas)

## Bounce and chatter

When you press a **mechanical** pushbutton, the metal contacts do not land once and stay closed. For a **short time** (often on the order of **milliseconds**) they can **open and close several times** before settling.

- **Bounce**: that brief period where the signal is unstable - “the button is bouncing.”
- **Chatter**: same idea - the contacts are **chattering** as they mate.

So **one** physical press can produce **many** short transitions on the wire the GPIO reads, not a single clean change.

## Edges

Think of the voltage on the input pin as a **logic level** over time: mostly **HIGH** (not pressed, with a pull-up) or **LOW** (pressed, tied to GND).

An **edge** is a **transition** between levels:

- **Falling edge** - HIGH -> LOW (press, in an active-low setup).
- **Rising edge** - LOW -> HIGH (release).

**Bounce** means you get **several** falling edges (and rising edges on release) where you only want **one** “logical” press or release. A **naïve** loop that counts every time it sees LOW can treat **one** physical press as **many** presses.

## Is debouncing just `sleep`?

**Partly, but not only.**

- A **short delay** after you first see a press gives the contacts time to **settle**; checking again after that delay is a classic **debounce** step.
- You also need **logic**: e.g. “count this press only if it is **still** the same button after the wait,” and “don’t treat the next sample as a new press until **all** buttons are **released**.”

So **sleep** is a **tool**; **debouncing** is the **policy** (wait + confirm + idle before next press).

## Why “only `sleep` once per loop” is not enough

Two separate issues get mixed together:

1. **Bounce** - one tap -> many quick LOW/HIGH flips. A loop that samples too fast can **count** multiple times before the contact settles.
2. **Hold** - if the loop body runs again while your finger is **still** holding the button, the pin stays LOW every time you check. Without a rule like “wait until released before the next press,” **one** long hold can look like **many** presses.

So debouncing is **not** only “sleep once”; you need **rules** that turn noisy transitions and continuous holds into **one logical press per tap**.

## Polling vs interrupts

In the Konami scripts (e.g. [Konami-Code-internal-pull-up-lgpio.py](Konami-Code-internal-pull-up-lgpio.py) with `lgpio.gpio_read`, or [Konami-internal-pull-up-rpigpio.py](Konami-internal-pull-up-rpigpio.py) with `GPIO.input`), the program **polls**: it runs a loop and **asks** each GPIO, over and over, “are you LOW right now?”. That is **software polling**.

**GPIO interrupts** (on the Pi, often via **edge detection** in the library) mean: you **register** a function (a **callback**) and the system runs it when the hardware detects a **rising** or **falling** edge on a pin - your main code does not have to sit in a tight `while True` reading pins.

- You still need **debouncing** in spirit: libraries often offer something like **`bouncetime`** (milliseconds to ignore repeated edges), and you still must avoid counting **one hold** as many events (often by handling **press** vs **release** or using a small state machine).

**Same wiring** for your breadboard: internal pull-up vs external pull-up does not change whether you poll or use interrupts - that is a **software** strategy on the same pins.

## What the Konami script does (summary)

See [04a-Explain-Py-Code-lgpio](04a-Explain-Py-Code-lgpio.md) for the main walkthrough (same ideas in [04b — gpiozero](04b-Explain-Py-Code-gpiozero.md) and [04c — RPi.GPIO](04c-Explain-Py-Code-rpigpio.md)). In short:

The whole issue is how to **not** count one hold as many presses, and **not** count bounce as many presses.

1. `wait_for_release()` — wait until **no** button reads as pressed (with a short debounce delay). Start each read from a known **idle** state.
2. `wait_for_press()` — detect a press; **bounce** is handled with a short delay and/or the library’s debounce (`gpio_set_debounce_micros` on **lgpio**, `bounce_time` on **gpiozero**, re-sample after `DEBOUNCE_S` on **RPi.GPIO** — see [04a](04a-Explain-Py-Code-lgpio.md)–[04c](04c-Explain-Py-Code-rpigpio.md)).
3. After a normal step, `wait_for_release()` again — so you do not immediately queue another “press” while the finger is still down (**hold** vs **new tap**).

Together that gives **one logical press per tap**, which is what you want for Konami. The structure is reasonable for tactile switches; it is not complexity for its own sake.

**Small caveat:** `read_pressed_button()` walks `pins` in dict order and returns the **first** LOW pin. If two buttons were pressed at once (unlikely in normal use), only one would “win.” Fine for this project.
