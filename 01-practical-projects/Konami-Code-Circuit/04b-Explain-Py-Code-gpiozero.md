# How `Konami-Code-internal-pull-up-gpiozero.py` works

This note walks through [Konami-Code-internal-pull-up-gpiozero.py](Konami-Code-internal-pull-up-gpiozero.py): **gpiozero**’s `Button` and `LED` classes instead of raw `lgpio` or `RPi.GPIO`. Behavior matches the **[lgpio](04a-Explain-Py-Code-lgpio.md)** and **[RPi.GPIO](04c-Explain-Py-Code-rpigpio.md)** versions.

## Imports

```python
from gpiozero import Button, LED
```

**gpiozero** uses BCM numbering by default for these devices.

## Construct `Button` and `LED` objects

```python
buttons = {
    name: Button(pin, pull_up=True, bounce_time=DEBOUNCE_S)
    for name, pin in PINS.items()
}

green = LED(GREEN_LED_PIN)
red = LED(RED_LED_PIN)
```

- **`pull_up=True`** - internal pull-up, same **active-low** idea: released = high, pressed = connects to GND → **`is_pressed`** is `True`.
- **`bounce_time=DEBOUNCE_S`** - library-side debouncing (seconds), so mechanical chatter is filtered before `is_pressed` stabilizes.

**`LED`** wraps a single output pin; **`.on()` / `.off()`** replace raw `GPIO.output`.

## Reading which button is down

```python
if btn.is_pressed:
    return name
```

Same “first match in dict order” rule if two buttons were ever active at once.

## `wait_for_release()` / `wait_for_press()`

Identical **structure** to the lgpio script: wait until nothing is pressed, then spin until something is pressed. **gpiozero** already applies **`bounce_time`** on the `Button` objects, so this pair mainly enforces **one tap → one step** and **release before the next press** (see [05-Debouncing](05-Debouncing.md)).

## LED helpers

- **`leds_off()`** — `green.off(); red.off()`
- **`blink_reset_ack()`** / **`blink_feedback(correct)`** — `(green if correct else red).on()` for a short sleep, then off.

## Main loop and Konami logic

Same as [04a](04a-Explain-Py-Code-lgpio.md): **RESET** clears the list (not in `KONAMI`); append + sliding window; prefix check → green/red; full sequence → **`green.on()`**, **`show_hire_me_fullscreen()`**, exit loop.

## Cleanup

```python
finally:
    leds_off()
    for btn in buttons.values():
        btn.close()
    green.close()
    red.close()
```

**gpiozero** expects devices **closed** to free GPIO resources cleanly.

## Summary

| Piece | Role |
|--------|------|
| `Button(..., pull_up=True, bounce_time=...)` | Active-low inputs + software debounce |
| `LED` | Outputs without manual `setup` |
| `is_pressed` | Polling (same game loop as other scripts) |
| `.close()` on each device | Clean exit |
