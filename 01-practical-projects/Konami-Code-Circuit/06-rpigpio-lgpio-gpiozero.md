# RPi.GPIO vs lgpio vs gpiozero (Debian 13 / newer kernels)

Modern Raspberry Pi kernels (e.g. on Debian Trixie/13) use the **GPIO character device** interface. The classic **RPi.GPIO** library historically relied on older kernel GPIO access paths and may not work (or may be missing) on newer systems.

This project therefore includes three “internal pull-up” variants that behave the same but use different libraries:

- `Konami-internal-pull-up-rpigpio.py`
- `Konami-Code-internal-pull-up-lgpio.py`
- `Konami-Code-internal-pull-up-gpiozero.py`

## What changes between the files

### Pin numbering

- All three versions use **BCM GPIO numbers** (the numbers from [pinout.xyz](https://pinout.xyz/)).

### Input setup (internal pull-ups, active-low)

- **RPi.GPIO**: `GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)` then `GPIO.input(pin) == GPIO.LOW`.
- **lgpio**: `gpio_claim_input(handle, pin, lgpio.SET_PULL_UP)` then `gpio_read(handle, pin) == 0`.
- **gpiozero**: `Button(pin, pull_up=True, ...)` then `btn.is_pressed` (pressed = `True`).

### Output setup (LEDs)

- **RPi.GPIO**: `GPIO.setup(led, GPIO.OUT)` + `GPIO.output(led, GPIO.HIGH/LOW)`.
- **lgpio**: `gpio_claim_output(handle, led, initial)` + `gpio_write(handle, led, 1/0)`.
- **gpiozero**: `LED(pin).on()` / `.off()`.

### Debouncing / “one tap = one step”

All three scripts enforce “**release before the next press**” (so holding a button doesn’t count repeatedly).

- **RPi.GPIO version** does debouncing in pure software: sleep a short window, then confirm the same key is still pressed.
- **lgpio version** optionally enables a built-in debounce filter (`gpio_set_debounce_micros` when available) and keeps the “release before next press” policy.
- **gpiozero version** uses `bounce_time=...` on each `Button` plus the same “release before next press” policy.

## Which should I use?

- Use **`lgpio`** on Debian 13 / modern kernels if you want a low-level, explicit GPIO API.
- Use **`gpiozero`** if you want the simplest code and higher-level primitives.
- Keep the **RPi.GPIO** file as a reference / legacy version (or for OS images where it still works).

