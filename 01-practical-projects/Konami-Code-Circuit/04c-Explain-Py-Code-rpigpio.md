# How `Konami-internal-pull-up-rpigpio.py` works

This note walks through [Konami-internal-pull-up-rpigpio.py](Konami-internal-pull-up-rpigpio.py): the classic **RPi.GPIO** API. The **game logic** (Konami list, sliding window, prefix LEDs, reset, Tk) is the same as **[04a — lgpio](04a-Explain-Py-Code-lgpio.md)** (recommended on new OS) and **[04b — gpiozero](04b-Explain-Py-Code-gpiozero.md)**.

## What the program does

The Pi reads **seven** inputs (four directions, **A**, **B**, **RESET**). Each physical **tap** should add **one** step to an internal list. The list is compared to the classic Konami sequence:

`UP, UP, DOWN, DOWN, LEFT, RIGHT, LEFT, RIGHT, B, A`

After each non-reset press, two LEDs give **immediate feedback**: green blink if that press still matches the beginning of the code up to that point; red if it does not. When the full sequence is correct, the script shows a **“Hire Me!”** fullscreen message if a desktop display is available.

## Imports and GPIO numbering

```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
```

**BCM** means “use Broadcom pin numbers” (the `GPIO` numbers in the pin table), not “physical pin 1-40.” That matches [03-Wiring-Hardware](03-Wiring-Hardware.md) and [pinout.xyz](https://pinout.xyz/).

## Inputs: `pins` and internal pull-ups

```python
pins = { "UP": 17, "DOWN": 27, ... "RESET": 5 }
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
```

On the breadboard, each button connects its GPIO to **GND** when pressed. With **`PUD_UP`**, the Pi weakly pulls the pin toward **3.3 V** when the button is **not** pressed, so the pin reads **HIGH** (idle). When you press, the pin is pulled to **GND** and reads **LOW**. That pattern is often called **active-low**.
The third parameter `pull_up_down=GPIO.PUD_UP` (or: `pull_up_down=GPIO.PUD_DOWN`) in the `GPIO.setup()` function sets the pull-up or pull-down resistor.  https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-api

**`RESET`** is a normal input like the others; it is not part of the Konami string but is handled specially in `main()` (see below).

## Outputs: LEDs

```python
GREEN_LED = 18
RED_LED = 16
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)
```

Each LED is wired GPIO -> resistor -> LED -> GND, so **HIGH** turns the LED **on**. The script starts with both off.

`leds_off()` just sets both GPIOs LOW so feedback flashes do not leave a LED stuck on by mistake.

## The Konami sequence as data

```python
KONAMI = ["UP", "UP", "DOWN", "DOWN", "LEFT", "RIGHT", "LEFT", "RIGHT", "B", "A"]
```

The program compares **names** (`"UP"`, `"DOWN"`, …) to this list, not raw pin numbers. That keeps the game logic readable.

## Why not read the button in one line in `main`?

Mechanical buttons **bounce**: for a few milliseconds the contact can chatter open/closed before it settles. If you only sampled the pin once per loop **as fast as possible**, one physical press might look like many quick LOW readings.

A second problem: if you **hold** a button, the pin stays LOW. A tight loop would see LOW over and over and could append the same step **many times per second**.

So the script separates:

1. **Debouncing** - wait a little and **confirm** the same button is still pressed (filters bounce).
2. **Waiting for release** - do not accept the **next** logical press until **no** button is pressed (turns one continuous hold into one logical press per tap, and gives a clean boundary between taps).

Those ideas are spelled out in [05-Debouncing](05-Debouncing.md). Here, **`DEBOUNCE_S = 0.05`** is the “ignore chatter, then re-check” window.

**Edge detection** (in the general sense: reacting to a **transition** press vs idle) is **not** implemented with hardware interrupt callbacks; the script uses **polling** - it repeatedly calls `GPIO.input()` in a loop. That is simpler to follow and enough for this project.

## `read_pressed_button()`

```python
for name, pin in pins.items():
    if GPIO.input(pin) == GPIO.LOW:
        return name
return None
```

This answers: “**Right now**, is any button pressed?” It walks the dictionary in **insertion order**. If two buttons were pressed at once (unusual), the **first** name in `pins` wins. For normal single-button use, that is fine.

## `wait_for_release()`

Sleep briefly, then loop until `read_pressed_button()` returns `None`. So the line is **idle** (no switch closed) before the next step. That is how the program enforces “**next** press only after you let go.”

## `wait_for_press()`

Loop until some button reads LOW; then **`sleep(DEBOUNCE_S)`** and check that the **same** button is still LOW. If yes, return that **one** logical press.

Together, `wait_for_release()` + `wait_for_press()` implement **one tap -> one list entry**, with debouncing.

## LED feedback helpers

- **`blink_reset_ack()`** - two quick green flashes after **RESET**, so you see the clear without mixing it into Konami green/red feedback.
- **`blink_feedback(correct)`** - one short green or red flash depending on whether the **current sequence** is still a correct **prefix** of `KONAMI`.

## `show_hire_me_fullscreen()`

Success is not only a `print`: on a Pi with a desktop session, `tkinter` can open a **fullscreen** window. If `python3-tk` is missing, or you are on SSH with no `DISPLAY`, the function falls back to printing a message instead. No GPIO change is required for that - it is display/environment only.

## `main()`: the real control flow

1. **`wait_for_release()`** - start from a clean idle state.
2. **`wait_for_press()`** - get **one** debounced press.
3. If **`RESET`**: clear `input_sequence`, flash the double green, **`wait_for_release()`**, **`continue`** (do not append RESET to the Konami list).
4. Otherwise **`append`** the press to `input_sequence`.
5. **`input_sequence = input_sequence[-len(KONAMI):]`** - keep at most the last **10** entries (length of Konami). Older presses drop off; that is a **sliding window** so a long wrong sequence does not grow forever.
6. **`correct_prefix = input_sequence == KONAMI[:n]`** - after this press, does the list equal the **first `n` elements** of the real code? That is the “still on track” test.
7. **`blink_feedback(correct_prefix)`** - show green or red for this step.
8. If **`input_sequence == KONAMI`**: success - leave green on (until exit), run the fullscreen hire message, **`break`** out of the loop.
9. If not done: **`wait_for_release()`** again so holding the key does not immediately count as the next press on the next iteration.

**`try` / `except KeyboardInterrupt` / `finally GPIO.cleanup()`** - Ctrl+C exits cleanly; `cleanup()` returns GPIOs to a safe state.

## Summary table

| Piece | Role |
|--------|------|
| `pins` + `PUD_UP` | Active-low buttons; idle HIGH, pressed LOW |
| `wait_for_release` + `wait_for_press` + `DEBOUNCE_S` | One logical press per tap; debounce; [05-Debouncing](05-Debouncing.md) |
| Sliding window slice | Only last 10 inputs matter |
| Prefix check vs `KONAMI[:n]` | Green = still matching from the start; red = derailed |
| `RESET` | Clears list; double green; not in Konami string |
| Tk fullscreen | Optional hire message when a GUI display exists |
