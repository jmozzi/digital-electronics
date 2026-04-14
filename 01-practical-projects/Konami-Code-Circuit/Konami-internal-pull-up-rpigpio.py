#!/usr/bin/env python3
"""
Konami code on Raspberry Pi 4: seven pushbuttons - U/D/L/R, A, B, and RESET (clears progress).
Green LED: blink = press continues the Konami sequence; red LED: blink = wrong press.
RESET clears the sequence (use after a mistake without waiting for a sliding-window match).
Requires: RPi.GPIO, and for fullscreen message: python3-tk (usually preinstalled on Desktop Pi OS).
Run on the Pi desktop session if you want the monitor message; over SSH without display, it falls back to console.
"""

import os
import sys
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# INPUT PINS: buttons - wired to GND when pressed, internal pull-up
pins = {
    "UP": 17,
    "DOWN": 27,
    "LEFT": 22,
    "RIGHT": 23,
    "B": 24,
    "A": 25,
    # Dedicated reset button - not part of Konami; clears progress
    "RESET": 5,
}

# OUTPUT PINS: each LED via resistor to GND; HIGH = on
GREEN_LED = 18
RED_LED = 16  # change if this BCM pin is already used on your breadboard

for pin in pins.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for led in (GREEN_LED, RED_LED):
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)


def leds_off():
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.output(RED_LED, GPIO.LOW)


KONAMI = ["UP", "UP", "DOWN", "DOWN", "LEFT", "RIGHT", "LEFT", "RIGHT", "B", "A"]

# Ignore electrical bounce (seconds)
DEBOUNCE_S = 0.05


def read_pressed_button():
    """Return name of button currently held low, or None."""
    for name, pin in pins.items():
        if GPIO.input(pin) == GPIO.LOW:
            return name
    return None


def wait_for_release():
    """Block until no input pin is pressed (stable idle)."""
    time.sleep(DEBOUNCE_S)
    while read_pressed_button() is not None:
        time.sleep(0.01)


def wait_for_press():
    """Block until a new press is detected, then debounce and return one logical press."""
    while True:
        pressed = read_pressed_button()
        if pressed is not None:
            time.sleep(DEBOUNCE_S)
            # Still pressed after debounce?
            if read_pressed_button() == pressed:
                return pressed
        time.sleep(0.01)


def blink_reset_ack() -> None:
    """Short double green flash: sequence was cleared."""
    leds_off()
    for _ in range(2):
        GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(0.06)
        leds_off()
        time.sleep(0.05)


def blink_feedback(correct: bool, duration: float = 0.1) -> None:
    """Flash green if this press keeps a valid Konami prefix; otherwise flash red."""
    leds_off()
    if correct:
        GPIO.output(GREEN_LED, GPIO.HIGH)
    else:
        GPIO.output(RED_LED, GPIO.HIGH)
    time.sleep(duration)
    leds_off()


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

    # Close after 30 s if untouched
    root.after(30_000, root.destroy)
    root.mainloop()


def main():
    input_sequence = []

    print(
        "Konami: ↑↑↓↓←→←→BA - one press per direction/button; "
        "RESET button clears the sequence. One logical press per tap (debounced)."
    )
    try:
        while True:
            # Wait for idle, then next single press (one entry per physical tap)
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

            # Sliding window: green if the last N inputs match the first N of Konami
            n = len(input_sequence)
            correct_prefix = input_sequence == KONAMI[:n]
            blink_feedback(correct_prefix, duration=0.1)

            if input_sequence == KONAMI:
                print("KONAMI - HIRE ME!")
                leds_off()
                GPIO.output(GREEN_LED, GPIO.HIGH)
                show_hire_me_fullscreen()
                break

            # Small pause so release is clean before next wait_for_release
            wait_for_release()

    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()

