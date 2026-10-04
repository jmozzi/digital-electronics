# How `Konami-Code-internal-pull-up-lgpio.py` works

This script uses the **lgpio** library which matches modern kernel expectations (see [06-rpigpio-lgpio-gpiozero](06-rpigpio-lgpio-gpiozero.md)).

## Imports

```python
import lgpio
```

No `GPIO.setmode(BCM)` — **lgpio** uses **Broadcom GPIO numbers** directly when you claim each line. The default chip is `/dev/gpiochip0`, opened below.

## Open the GPIO chip and claim lines

```python
h = lgpio.gpiochip_open(0)
```

`0` is the first GPIO chip (typical on a Pi). `h` is a handle passed to every later `lgpio.*` call.

**Inputs** — for each BCM number in `PINS`:

```python
lgpio.gpio_claim_input(h, gpio, lgpio.SET_PULL_UP)
```

- **`SET_PULL_UP`** matches **active-low** wiring: idle ≈ high, pressed = tied to GND -> reads **0**.
- The script still uses **wait-for-release** in software so one physical tap counts once.

**Outputs** (LEDs):

```python
lgpio.gpio_claim_output(h, led, 0)
```

Initial level **0** = LEDs off (assuming GPIO -> resistor -> LED -> GND).

Nested **`leds_off()`** uses `lgpio.gpio_write(h, pin, 0)` on both LED pins.

## Reading buttons

```python
if lgpio.gpio_read(h, gpio) == 0:
```

Pressed = **0** (active-low). Same idea as `GPIO.LOW` in RPi.GPIO, different API.

**`read_pressed_button()`** walks `PINS` in order; if two switches are closed, the **first** name in the dict wins.

## `wait_for_release()` and `wait_for_press()`

Same **control-flow goal** as the other scripts: one **logical** press per physical tap — see [05-Debouncing](05-Debouncing.md).

- **`wait_for_release()`** — short sleep, then loop until **no** button reads pressed (`gpio_read` all non-zero).
- **`wait_for_press()`** — spin until **some** button reads pressed, then return its name. Debounce is partly delegated to **`gpio_set_debounce_micros`** where available; release-then-next-press avoids hold-to-repeat.

*(The RPi.GPIO version re-samples after `DEBOUNCE_S` inside `wait_for_press`; this lgpio build leans on the optional microsecond debounce plus release gating.)*

## LED feedback

- **`blink_reset_ack()`** — two quick green flashes after **RESET**.
- **`blink_feedback(correct)`** — one short green **or** red flash via `gpio_write(..., 1)` then off.

## `show_hire_me_fullscreen()`

Same Tk fullscreen / fallback `print` as the other variants — **no GPIO** involved; only checks `DISPLAY` / `WAYLAND_DISPLAY`

## `main()` loop

1. **`wait_for_release()`** -> **`wait_for_press()`**
2. **`RESET`** -> clear list, double green, `continue` (not appended to Konami).
3. Else **append**, **slice** to last `len(KONAMI)` inputs (sliding window).
4. **`correct_prefix = input_sequence == KONAMI[:n]`** -> green vs red blink.
5. Full match -> green steady, Tk message, **`break`**.
6. Else **`wait_for_release()`** before next iteration.

## Cleanup

```python
finally:
    lgpio.gpio_write(h, GREEN_LED, 0)
    lgpio.gpio_write(h, RED_LED, 0)
    lgpio.gpiochip_close(h)
```

Turns LEDs off and **releases the chip** (unlike `RPi.GPIO.cleanup()` naming, but same intent: leave hardware safe).

**Ctrl+C** -> `KeyboardInterrupt` -> same `finally` runs.

## Summary

| Piece | Role |
|--------|------|
| `gpiochip_open` / `gpiochip_close` | Own the GPIO chip for this process |
| `gpio_claim_input` + `SET_PULL_UP` | Active-low buttons |
| `gpio_claim_output` | LEDs |
| `gpio_read` / `gpio_write` | Read buttons, drive LEDs |
| Sliding window + prefix check | Same Konami logic as [04b](04b-Explain-Py-Code-gpiozero.md) / [04c](04c-Explain-Py-Code-rpigpio.md) |
