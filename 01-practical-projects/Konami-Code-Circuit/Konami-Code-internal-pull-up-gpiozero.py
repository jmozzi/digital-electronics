#!/usr/bin/env python3
"""
Konami code (internal pull-ups) using gpiozero.

Buttons are wired to GND when pressed (active-low) and use internal pull-ups.
gpiozero provides built-in bounce handling via Button(bounce_time=...).
"""

import os
import sys
import time

from gpiozero import Button, LED


PINS = {
    "UP": 17,
    "DOWN": 27,
    "LEFT": 22,
    "RIGHT": 23,
    "B": 24,
    "A": 25,
    "RESET": 5,
}

GREEN_LED_PIN = 18
RED_LED_PIN = 16

KONAMI = ["UP", "UP", "DOWN", "DOWN", "LEFT", "RIGHT", "LEFT", "RIGHT", "B", "A"]

DEBOUNCE_S = 0.05


def show_hire_me_fullscreen():
    """Show message on attached monitor if Tk + display available."""
    try:
        import tkinter as tk
    except ImportError:
        print("HIRE ME! (install python3-tk for on-screen text)")
        return

    has_display = "DISPLAY" in os.environ or "WAYLAND_DISPLAY" in os.environ
    if not (sys.platform == "linux" and has_display):
        print("HIRE ME! (no GUI display; connect a monitor or set DISPLAY)")
        return

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Button-1>", lambda e: root.destroy())

    label = tk.Label(
        root,
        text="Hire Me!",
        fg="#00ff66",
        bg="black",
        font=("Sans", 72, "bold"),
    )
    label.pack(expand=True)
    root.after(30_000, root.destroy)
    root.mainloop()


def main():
    buttons = {
        name: Button(pin, pull_up=True, bounce_time=DEBOUNCE_S)
        for name, pin in PINS.items()
    }

    green = LED(GREEN_LED_PIN)
    red = LED(RED_LED_PIN)

    def leds_off():
        green.off()
        red.off()

    def read_pressed_button():
        """Return name of button currently held down, or None."""
        for name, btn in buttons.items():
            if btn.is_pressed:
                return name
        return None

    def wait_for_release():
        # bounce_time already suppresses chatter; this enforces "one tap -> one step"
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
            green.on()
            time.sleep(0.06)
            leds_off()
            time.sleep(0.05)

    def blink_feedback(correct: bool, duration: float = 0.1):
        leds_off()
        (green if correct else red).on()
        time.sleep(duration)
        leds_off()

    input_sequence: list[str] = []

    print(
        "Konami: ↑↑↓↓←→←→BA - one press per direction/button; "
        "RESET button clears the sequence. One logical press per tap (debounced)."
    )

    try:
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
                print("KONAMI - HIRE ME!")
                leds_off()
                green.on()
                show_hire_me_fullscreen()
                break

            wait_for_release()

    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        leds_off()
        for btn in buttons.values():
            btn.close()
        green.close()
        red.close()


if __name__ == "__main__":
    main()

