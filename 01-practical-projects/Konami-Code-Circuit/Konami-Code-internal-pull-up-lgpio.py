#!/usr/bin/env python3
"""
Konami code (internal pull-ups) using lgpio.

This is a modern-kernel alternative to the RPi.GPIO version.
Buttons are wired to GND when pressed (active-low) and use internal pull-ups.
"""

import os
import sys
import time

import lgpio


# INPUT PINS: buttons - wired to GND when pressed, internal pull-up
PINS = {
    "UP": 17,
    "DOWN": 27,
    "LEFT": 22,
    "RIGHT": 23,
    "B": 24,
    "A": 25,
    # Dedicated reset button - not part of Konami; clears progress
    "RESET": 5,
}

# OUTPUT PINS: each LED via resistor to GND; 1 = on
GREEN_LED = 18
RED_LED = 16  # change if this BCM pin is already used on your breadboard

KONAMI = ["UP", "UP", "DOWN", "DOWN", "LEFT", "RIGHT", "LEFT", "RIGHT", "B", "A"]

# Debounce window (seconds).
# lgpio can apply a hardware-side debounce filter (in microseconds); we also keep a simple
# "release before next press" policy so one hold counts once.
DEBOUNCE_S = 0.05


def show_hire_me_fullscreen():
    """Show message on attached monitor if Tk + display available."""
    try:
        import tkinter as tk
    except ImportError:
        print("k0n4m164 :) Hire Me! (install python3-tk for on-screen text)")
        return

    has_display = "DISPLAY" in os.environ or "WAYLAND_DISPLAY" in os.environ
    if not (sys.platform == "linux" and has_display):
        print("k0n4m164 :) Hire Me! (no GUI display; connect a monitor or set DISPLAY)")
        return

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Button-1>", lambda e: root.destroy())

    label = tk.Label(
        root,
        text="k0n4m164 :) Hire Me!",
        fg="#00ff66",
        bg="black",
        font=("Sans", 72, "bold"),
    )
    label.pack(expand=True)

    root.after(30_000, root.destroy)
    root.mainloop()


def main():
    h = lgpio.gpiochip_open(0)
    try:
        # Claim inputs with pull-ups (active-low buttons)
        debounce_micros = int(DEBOUNCE_S * 1_000_000)
        for gpio in PINS.values():
            lgpio.gpio_claim_input(h, gpio, lgpio.SET_PULL_UP)
            # Optional built-in debounce/glitch filter (if supported by this lgpio build).
            try:
                lgpio.gpio_set_debounce_micros(h, gpio, debounce_micros)
            except AttributeError:
                pass

        # Claim outputs (LEDs)
        for led in (GREEN_LED, RED_LED):
            lgpio.gpio_claim_output(h, led, 0)

        def leds_off():
            lgpio.gpio_write(h, GREEN_LED, 0)
            lgpio.gpio_write(h, RED_LED, 0)

        def read_pressed_button():
            """Return name of button currently held low (0), or None."""
            for name, gpio in PINS.items():
                if lgpio.gpio_read(h, gpio) == 0:
                    return name
            return None

        def wait_for_release():
            time.sleep(DEBOUNCE_S)
            while read_pressed_button() is not None:
                time.sleep(0.01)

        def wait_for_press():
            while True:
                pressed = read_pressed_button()
                if pressed is not None:
                    return pressed
                time.sleep(0.01)

        def blink_reset_ack():
            leds_off()
            for _ in range(2):
                lgpio.gpio_write(h, GREEN_LED, 1)
                time.sleep(0.06)
                leds_off()
                time.sleep(0.05)

        def blink_feedback(correct: bool, duration: float = 0.1):
            leds_off()
            lgpio.gpio_write(h, GREEN_LED if correct else RED_LED, 1)
            time.sleep(duration)
            leds_off()

        input_sequence: list[str] = []

        print(
            "Konami: ↑↑↓↓←→←→BA - one press per direction/button; "
            "RESET button clears the sequence. One logical press per tap (debounced)."
        )

        while True:
            wait_for_release()
            press = wait_for_press()

            print("Pressed:", press)

            if press == "RESET":
                input_sequence = []
                print("Reset - sequence cleared.")
                blink_reset_ack()
                wait_for_release()
                continue

            input_sequence.append(press)
            input_sequence = input_sequence[-len(KONAMI) :]

            n = len(input_sequence)
            correct_prefix = input_sequence == KONAMI[:n]
            blink_feedback(correct_prefix, duration=0.1)

            if input_sequence == KONAMI:
                print("k0n4m164 :) Hire Me!")
                leds_off()
                lgpio.gpio_write(h, GREEN_LED, 1)
                show_hire_me_fullscreen()
                break

            wait_for_release()

    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        # Ensure LEDs off and chip closed.
        try:
            lgpio.gpio_write(h, GREEN_LED, 0)
            lgpio.gpio_write(h, RED_LED, 0)
        except Exception:
            pass
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()

